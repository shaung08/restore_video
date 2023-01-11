

### system flow
1. 輸入影片
2. 選擇影片要縮放的比例和剪裁的位置
3. 如果影片的fps大於30，降低至fps=30
4. 輸入影片到mmedit，提高影片畫質
5. 將音檔加入mmedit後的影片，輸出最終結果


### 紀錄
-r: 設定output的framerate，不改變影片時間長度
-crf: 數值越大壓縮的越多，18~28是一個合理的範圍
crop: crop=<width>:<height>:<x>:<y>

```
$ ffmpeg -i input_Trim.mp4 -filter_complex "[0:v]crop=377:720:0:0[cropped]" -map "[cropped]" -vcodec libx264  -crf 18 -r 24 output04.mp4
```