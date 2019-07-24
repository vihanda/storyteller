import os
import ffmpeg

class VideoCreator(object):
    def __init__(self, project_directory):
        self.images_directory = project_directory

    def make_video(self):
        command = ("ffmpeg.exe -framerate 1/5 -i {0}/*.jpg -c:v libx264 -r 30 -pix_fmt yuv420p {0}/out.mp4").format(self.images_directory)
        os.system(command)

    def add_music(self):
        command = ("ffmpeg.exe -i {0}/out.mp4 -i {0}/music.ogg -c copy -map 0:v:0 -map 1:a:0 {0}/final_video.mp4").format(self.images_directory)
        os.system(command)
        