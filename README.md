# Document
## Introduction
影片長度若為 10 分鐘以內，則其檔案大小上限為 650 MB。影片長度若長達 60 分鐘，則其檔案大小上限為 3.6 GB。

### instragram video requirement 
1. 您可以上傳長寬比介於 1.91:1 與 9:16 的影片。
2. 影片的影格速率最低為 30 FPS（每秒影格數），而最低解析度則為 720 像素。
3. 輸出最大長度為60秒。
4. 影片長度若為10 分鐘以內，則其檔案大小上限為650 MB。 影片長度若長達60 分鐘，則其檔案大小上限為3.6 GB。

### Input
1. 原始影片大於720畫素
2. 原始影片大於30FPS
3. ig個人帳戶選擇上傳最佳影片畫質

### Output
1. 輸出 *.mp4 檔案 (影像H.264編碼 30FPS、音訊AAC-LC編碼)
補充mp4格式: 混合與串流，同時可以支援存放字幕。支援的影像編碼包含 H.26X、MPEG-4 Part2、VP9；支援的聲音編碼包含 AAC、MPEG-4 Part3。
1. 輸出最大長度為60秒

## Tools
### video encoder
image encoder (H.264)
1. 漸進式掃描（不支援交錯式掃描）。
2. 高組態。
3. 連續 2 個 B 畫格。
4. 封閉式 GOP。
5. 影格速率一半的 GOP。
6. CABAC。
7. 色度抽樣：4:2:0。

Audio encoder (AAC-LC編碼)
1. 聲道：立體聲或立體聲 + 5.1 聲道。
2. 取樣率：96 khz 或 48 khz。

## Test
1. 壓縮完影片測試是否還會被ig壓縮。
2. 壓縮影片後套濾鏡，當檔案變大時，是否會被ig壓縮影片?

## Installation
docker installation(recommand)

### Pull images and run container 
```
$ docker pull pytorch/pytorch:1.7.1-cuda11.0-cudnn8-devel
$ docker run -it --gpus all --shm-size=8g nvidia/cuda:11.4.0-devel-ubuntu20.04 bash
```

### Install requirements
```
$ apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub && apt-get update && apt-get install -y git ninja-build libglib2.0-0 libsm6 libxrender-dev libxext6 libgl1-mesa-glx && rm -rf /var/lib/apt/lists/*
$ apt install ffmpeg

$ git clone -b v1.0.0rc4 https://github.com/open-mmlab/mmediting.git /mmediting
$ cd /mmediting/
$ pip install --upgrade pip
$ pip3 install openmim
$ mim install mmcv-full==1.5.0
$ pip3 install -e .
```

### execute
```
$ python main.py -c mmedit/configs/basicvsr_pp/basicvsr-pp_c64n7_8xb1-600k_reds4.py -w basicvsr_plusplus_c64n7_8x1_600k_reds4_20210217-db622b2f.pth -i input_Trim.mp4 -o /home/output01.mp4 --max-seq-len 20
```
