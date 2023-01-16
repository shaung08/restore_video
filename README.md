# Document
## System: ubuntu18.04
## Introduction
When uploading video on instagram, it always decompresses video resolution. This repo wants to optimize the origin video resolution and 
follows the Instagram video [compressing rules](#instragram-video-requirement), so that video maintain the same quality as it uploaded on instagram. 

This repo using [open-mmlab/mmediting](https://github.com/open-mmlab/mmediting) to optimizes video resolution. 

## Installation
## docker installation
1. pull and run docker images.
note: set `<frontned-port>` to opend web service and `<backend-port>` to connect backend service.
```
$ docker pull qctuser/restore-video
$ docker run -it -p <frontned-port>:9010 -p <backend-port>:9000 qctuser/restore-video bash
```
2. Set `<hostip>` and `<backend-port>` in `/home/restore_video/frontend/src/utils/ip.js`
```
const ip="<hostip>:<backend-port>"
export default ip;
```
3. execute service
```
$ /home/restore_video/start.sh
```
4. open browser and web protocol `http://<hostip>:<frontned-port>`
