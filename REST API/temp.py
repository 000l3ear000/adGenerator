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


RESIZED_VIDEO = "Template 1.mov";

for i in range( 20 ):
    video = VideoFileClip( "Template " + str( i  + 1 ) + ".mov" )
    res = CompositeVideoClip([video])
    res.write_videofile( "Template_" + str( i + 1 ) + ".webM", bitrate="50000k", fps=24 )
