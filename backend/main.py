# Copyright (c) OpenMMLab. All rights reserved.
import os
import cv2
import mmcv
import numpy as np
import torch

from utils.argments import parse_args
from restore_video.backend.utils.convert_framerate import Video
from restore_video.backend.mmedit.apis import init_model, restoration_video_inference
from restore_video.backend.mmedit.utils import tensor2img

def main():
    """Demo for video restoration models.

    Note that we accept video as input/output, when 'input_dir'/'output_dir' is
    set to the path to the video. But using videos introduces video
    compression, which lowers the visual quality. If you want actual quality,
    please save them as separate images (.png).
    """
    tmp_video01, tmp_video02, fps = "source_tmp01.mp4", "source_tmp02.mp4", 24
    VIDEO_EXTENSIONS = ('.mp4', '.mov')
    args = parse_args()
    print(tmp_video01)

    tmp_video01 = os.path.join(args.tmpf ,tmp_video01)
    tmp_video02 = os.path.join(args.tmpf ,tmp_video02)
    video_ = Video(args.input, args.output, tmp_video01, tmp_video02, fps)
    video_.convert_framerate(args.x, args.y, args.width, args.height)

    if args.device < 0 or not torch.cuda.is_available():
        device = torch.device('cpu')
    else:
        device = torch.device('cuda', args.device)

    model = init_model(args.config, args.weights, device=device)

    rsv_i = restoration_video_inference(args.window_size, tmp_video01, model, args.max_seq_len)
    rsv_i.build_pipeline(args.start_idx, args.filename_tmpl)
    output = rsv_i.batch_forward_model()
    file_extension = os.path.splitext(args.output)[1]
    if file_extension in VIDEO_EXTENSIONS:  # save as video
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        h, w = output.shape[-2:]
        video_writer = cv2.VideoWriter(tmp_video02, fourcc, fps, (w, h))
        for i in range(0, output.size(1)):
            img = tensor2img(output[:, i, :, :, :])
            video_writer.write(img.astype(np.uint8))
        cv2.destroyAllWindows()
        video_writer.release()
        video_.combine_video()
    else:
        for i in range(args.start_idx, args.start_idx + output.size(1)):
            output_i = output[:, i - args.start_idx, :, :, :]
            output_i = tensor2img(output_i)
            save_path_i = f'{args.output}/{args.filename_tmpl.format(i)}'
            mmcv.imwrite(output_i, save_path_i)

if __name__ == '__main__':
    main()
