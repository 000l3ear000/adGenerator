import queue
from sys import argv
from os import path, remove
from moviepy.video.io.ffmpeg_tools import ffmpeg_resize
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeAudioClip, CompositeVideoClip, concatenate_videoclips, ImageClip
from moviepy.video.fx.mask_color import mask_color
from moviepy.video.fx.all import fadein, fadeout
from multiprocessing import Process, set_start_method, Queue
from math import ceil
import shutil


RESIZED_VIDEO = "resized.mp4"
lst = []
videoInput = "video1.mp4"

print("abc")
# python .\testMoviepy.py Template_10.webM "Text 1","Text 2","Text 3","Text 4","Text 5" video1.mp4 Cute.mp3 "50","green","fadeout","Courier-New","ad.mp4" 1
def resizeUserVideo(userVid, q):
   

    if path.exists(RESIZED_VIDEO):
        remove(RESIZED_VIDEO)

        ffmpeg_resize(userVid, RESIZED_VIDEO, [1080, 1080])

        print("i wa sher")
        result = VideoFileClip(RESIZED_VIDEO, audio=False).subclip(0, 10)
        lst.append(result)
        q.put(lst)
        print("result entered")

def f1():
    q = Queue()
    a = Process(target=resizeUserVideo, args=(videoInput,q))
    a.start()
    print(q.get())
    # print(lst[0])
    a.join()
    print("ok")
    print(q.get())
    # print(lst[0])


if __name__ == '__main__':
    set_start_method("spawn")
    cb = Process(target=f1)
    cb.start()
    # print(lst[0])
    cb.join()
    # print(lst[0])