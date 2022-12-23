# Copyright (c) OpenMMLab. All rights reserved.
# yapf: disable
from .inference_functions import (delete_cfg, init_model, restoration_video_inference)
# yapf: enable

__all__ = [
    'init_model', 'delete_cfg', 'restoration_video_inference'
]
