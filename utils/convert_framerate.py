import os
import ffmpeg

from moviepy.editor import *

class Video:
    def __init__(self, input_filename, output_filename, tmp_01, tmp_02, fps=30):
        self.input_filename = input_filename
        self.output_filename = output_filename
        self.tmp_01 = tmp_01
        self.tmp_02 = tmp_02
        self.fps = fps

    def convert_framerate(self):
        process = (ffmpeg.input(self.input_filename)
        .filter('fps', fps=self.fps, round='up')
        .output(self.tmp_01, **{'c:v': 'libx264'}, crf=18))
        process.run()

    def combine_video(self):
        audio = VideoFileClip(self.input_filename).audio
        video = VideoFileClip(self.tmp_02)
        output = video.set_audio(audio)
        output.write_videofile(self.output_filename, fps=self.fps,
                        temp_audiofile="temp-audio.m4a", 
                        remove_temp=True, codec="libx264", 
                        audio_codec="aac")

    def remove_tmp_file(self):
        pass