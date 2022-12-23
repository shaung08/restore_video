# Copyright (c) OpenMMLab. All rights reserved.
import glob
import os.path as osp

import mmcv
import numpy as np
import torch
from mmengine import Config
from mmengine.config import ConfigDict 
from mmengine.dataset import Compose 
from mmengine.fileio import FileClient
from mmengine.runner import load_checkpoint 

from restore_video.mmedit.utils import register_all_modules
from mmedit.registry import MODELS

VIDEO_EXTENSIONS = ('.mp4', '.mov', '.avi')
FILE_CLIENT = FileClient('disk')


def delete_cfg(cfg, key='init_cfg'):
    """Delete key from config object.

    Args:
        cfg (str or :obj:`mmengine.Config`): Config object.
        key (str): Which key to delete.
    """

    if key in cfg:
        cfg.pop(key)
    for _key in cfg.keys():
        if isinstance(cfg[_key], ConfigDict):
            delete_cfg(cfg[_key], key)


def init_model(config, checkpoint=None, device='cuda:0'):
    """Initialize a model from config file.

    Args:
        config (str or :obj:`mmengine.Config`): Config file path or the config
            object.
        checkpoint (str, optional): Checkpoint path. If left as None, the model
            will not load any weights.
        device (str): Which device the model will deploy. Default: 'cuda:0'.

    Returns:
        nn.Module: The constructed model.
    """

    if isinstance(config, str):
        config = Config.fromfile(config)
    elif not isinstance(config, Config):
        raise TypeError('config must be a filename or Config object, '
                        f'but got {type(config)}')
    # config.test_cfg.metrics = None
    delete_cfg(config.model, 'init_cfg')

    register_all_modules()
    model = MODELS.build(config.model)

    if checkpoint is not None:
        checkpoint = load_checkpoint(model, checkpoint)

    model.cfg = config  # save the config in the model for convenience
    model.to(device)
    model.eval()

    return model

def pad_sequence(data, window_size):
    """Pad frame sequence data.

    Args:
        data (Tensor): The frame sequence data.
        window_size (int): The window size used in sliding-window framework.

    Returns:
        data (Tensor): The padded result.
    """

    padding = window_size // 2

    data = torch.cat([
        data[:, 1 + padding:1 + 2 * padding].flip(1), data,
        data[:, -1 - 2 * padding:-1 - padding].flip(1)
    ],
                     dim=1)

    return data


class restoration_video_inference:
    def __init__(self, window_size, img_dir, model, max_seq_len=None):
        self.window_size = window_size
        self.img_dir = img_dir
        self.data = dict(img=[], img_path=None, key=img_dir)
        self.model = model
        self.max_seq_len = max_seq_len
        self.device = next(self.model.parameters()).device

    def build_pipeline(self, start_idx, filename_tmpl):
        # build the data pipeline
        if self.model.cfg.get('demo_pipeline', None):
            test_pipeline = self.model.cfg.demo_pipeline
        elif self.model.cfg.get('test_pipeline', None):
            test_pipeline = self.model.cfg.test_pipeline
        else:
            test_pipeline = self.model.cfg.val_pipeline

        # check if the input is a video
        file_extension = osp.splitext(self.img_dir)[1]
        if file_extension in VIDEO_EXTENSIONS:
            video_reader = mmcv.VideoReader(self.img_dir)
            # load the images
            
            for frame in video_reader:
                self.data['img'].append(np.flip(frame, axis=2))

            # remove the data loading pipeline
            tmp_pipeline = []
            for pipeline in test_pipeline:
                if pipeline['type'] not in [
                        'GenerateSegmentIndices', 'LoadImageFromFile'
                ]:
                    tmp_pipeline.append(pipeline)
            test_pipeline = tmp_pipeline
        else:
            # the first element in the pipeline must be 'GenerateSegmentIndices'
            if test_pipeline[0]['type'] != 'GenerateSegmentIndices':
                raise TypeError('The first element in the pipeline must be '
                                f'"GenerateSegmentIndices", but got '
                                f'"{test_pipeline[0]["type"]}".')

            # specify start_idx and filename_tmpl
            test_pipeline[0]['start_idx'] = start_idx
            test_pipeline[0]['filename_tmpl'] = filename_tmpl

            # prepare data
            sequence_length = len(glob.glob(osp.join(self.img_dir, '*')))
            lq_folder = osp.dirname(self.img_dir)
            key = osp.basename(self.mg_dir)
            self.data = dict(
                img_path=lq_folder,
                gt_path='',
                key=key,
                sequence_length=sequence_length)

        # compose the pipeline
        test_pipeline = Compose(test_pipeline)
        self.data = test_pipeline(self.data)
        self.data = self.data['inputs'].unsqueeze(0) / 255.0  # in cpu

    def batch_forward_model(self):
        # forward the model
        with torch.no_grad():
            if self.window_size > 0:  # sliding window framework
                self.data = pad_sequence(self.data, self.window_size)
                result = []
                for i in range(0, self.data.size(1) - 2 * (self.window_size // 2)):
                    data_i = self.data[:, i:i + self.window_size].to(self.device)
                    result.append(self.model(inputs=data_i, mode='tensor').cpu())
                result = torch.stack(result, dim=1)
            else:  # recurrent framework
                if self.max_seq_len is None:
                    result = self.model(inputs=self.data.to(self.device), mode='tensor').cpu()
                else:
                    result = []
                    for i in range(0, self.data.size(1), self.max_seq_len):
                        result.append(
                            self.model(
                                inputs=self.data[:, i:i + self.max_seq_len].to(self.device),
                                mode='tensor').cpu())
                    result = torch.cat(result, dim=1)
        return result