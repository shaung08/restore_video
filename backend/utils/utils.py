
import os
import uuid

def check_folder(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def save_video(upload_file, filename, coordinate):
    root = os.path.join("output", "tmp")
    check_folder(root)
    tmp_video = os.path.join("output", "tmp", "source.mp4")
    upload_file.save(tmp_video)
    
    os.system("python main.py -c configs/basicvsr_pp/basicvsr-pp_c64n7_8xb1-600k_reds4.py \
        -w basicvsr_plusplus_c64n7_8x1_600k_reds4_20210217-db622b2f.pth \
        -i %s \
        -o output/output.mp4 \
        --tmpf %s \
        --width %s \
        --height %s \
        --x %s \
        --y %s \
        --max-seq-len 20" \
        %(tmp_video, root, coordinate["width"], coordinate["height"], coordinate["x"], coordinate["y"]))
