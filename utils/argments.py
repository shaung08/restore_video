import argparse

# Copyright (c) OpenMMLab. All rights reserved.
import re
import sys
import warnings


def modify_args():
    """Modify args of argparse.ArgumentParser."""
    for i, v in enumerate(sys.argv):
        if i == 0:
            assert v.endswith('.py')
        elif re.match(r'--\w+_.*', v):
            new_arg = v.replace('_', '-')
            warnings.warn(
                f'command line argument {v} is deprecated, '
                f'please use {new_arg} instead.',
                category=DeprecationWarning,
            )
            sys.argv[i] = new_arg


def parse_args():
    modify_args()
    parser = argparse.ArgumentParser(description='Restoration demo')
    parser.add_argument('-c', '--config', help='test config file path')
    parser.add_argument('-w', '--weights', help='checkpoint file')
    parser.add_argument('-i', '--input', help='directory of the input video')
    parser.add_argument('-o', '--output', help='directory of the output video')
    parser.add_argument(
        '--start-idx',
        type=int,
        default=0,
        help='index corresponds to the first frame of the sequence')
    parser.add_argument(
        '--filename-tmpl',
        default='{:08d}.png',
        help='template of the file names')
    parser.add_argument(
        '--window-size',
        type=int,
        default=0,
        help='window size if sliding-window framework is used')
    parser.add_argument(
        '--max-seq-len',
        type=int,
        default=None,
        help='maximum sequence length if recurrent framework is used')
    parser.add_argument('--device', type=int, default=0, help='CUDA device id')
    args = parser.parse_args()
    return args