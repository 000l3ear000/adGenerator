from sys import argv
from os import path
from moviepy.video.io.ffmpeg_tools import ffmpeg_resize
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeAudioClip, CompositeVideoClip, concatenate_videoclips, ImageClip
from moviepy.video.fx.mask_color import mask_color
from moviepy.video.fx.all import fadein, fadeout
from adGeneratorConstants import epicDict, textMovements, textMovementsRight, textMovementsLeft, videoFormats, imageFormats
from multiprocessing import cpu_count
from math import ceil
import shutil

HEIGHT = 920
FONTSIZE = 70
FONTCOLOR = "white"
RESIZED_VIDEO = ""
LOGO = "logo.png"
THREADS = cpu_count()

# Template_16.webM "Text 1","Text 2","Text 3","Text 4","Text 5" video1.mp4 Cute.mp3 "50","green","fadeout"

if argv.__len__() > 5:

    templateName = argv[1]
    textArray = argv[2].split(',')
    videoInput = argv[3]
    RESIZED_VIDEO = argv[3][8:]
    audioClip = argv[4]
    fontProperties = argv[5].split(',')
    fontSize = int(fontProperties[0])
    fontColor = fontProperties[1]
    fontEffect = fontProperties[2]
    fontStyle = fontProperties[3]
    OUTPUT_FILE_NAME = fontProperties[4]
    previewFlag = argv[6] if argv.__len__() == 7 else 0

    print("printing data >>> ",fontSize, fontColor, fontEffect, fontStyle, OUTPUT_FILE_NAME, previewFlag)
    print("printing video info >>> ",templateName, textArray, videoInput, audioClip, previewFlag)


def calculate_height(fontSize):
    return returnHeight(templateName) - (fontSize / 2)


def returnTextTiming(templateName):
    temp = epicDict[templateName]
    return temp[0]


def returnSetStart(templateName):
    temp = epicDict[templateName]
    return temp[1]


def returnMaskColor(templateName):
    temp = epicDict[templateName]
    return temp[2]

def returnHeight(templateName):
    temp = epicDict[templateName]
    return temp[3]

def checkInputFile(fileName):
    ext = fileName.split('.')
    if ext[1] in videoFormats:
        return 1
    elif ext[1] in imageFormats:
        return 2
    else:
        return 0
 
def modifyDuration( vid ):
    duration = VideoFileClip( vid, audio=False ).duration
    if duration < 30:
        if previewFlag:
            return ceil( 10 / duration )
        else:
            return ceil( 30 / duration )
    else:
        return 0

def resizeUserVideo(userVid):
    if checkInputFile(userVid) == 1:

        ffmpeg_resize(userVid, RESIZED_VIDEO, [1080, 1080])
        duration = modifyDuration( userVid )
        clips = []
        if duration:
            for i in range(duration):
                clip = VideoFileClip( RESIZED_VIDEO, audio=False )
                clips.append(clip)
            final_clip = concatenate_videoclips( clips )
        
        if previewFlag and duration:
            return final_clip
        elif previewFlag and not(duration):
            print("i was here1")
            return VideoFileClip(RESIZED_VIDEO, audio=False).subclip(0, 10)
        else:
            if not(previewFlag) and duration:
                print("i was here2")
                return final_clip
            else:
                print("i was here3")
                return VideoFileClip(RESIZED_VIDEO, audio=False)

    elif checkInputFile(userVid) == 2:
        if previewFlag:
            return ImageClip(userVid).resize((1080, 1080)).subclip(0, 10)
        else:
            return ImageClip(userVid).resize((1080, 1080))
    else:
        return "unknown file uploaded"


def returnMaskedClip(fileName):
    if previewFlag:
        template = VideoFileClip(fileName).subclip(0, 10)
    else:
        template = VideoFileClip(fileName)
    masked_clip = mask_color(template, returnMaskColor(
        fileName), thr=100, s=5).set_opacity(.9)
    return masked_clip


def checkEffect():
    if fontEffect == "fadein":
        return True
    else:
        return False

def setText(fileName):
    clip_list = []
    timingArray = returnTextTiming(fileName)

    for text in range(timingArray.__len__()):
        # slicing the array to exlude double quotes
        txt_clip = TextClip(textArray[text][ 1 : -1], fontsize=fontSize, font=fontStyle,
                            color=fontColor).set_duration(timingArray[text])

        if checkEffect():
            txt_clip = fadein(txt_clip, 2, [255, 255, 0])
        else:
            txt_clip = fadeout(txt_clip, 2, [255, 255, 0])
        clip_list.append(txt_clip)

    final_clip = concatenate_videoclips(clip_list)
    return final_clip


def setTextRL(fileName):
    clip_list = []
    timingArray = returnTextTiming(fileName)

    for text in range(timingArray.__len__()):

        txt_clip = (TextClip(textArray[text][ 1 : -1], fontsize=fontSize, font=fontStyle,
                             color=fontColor).set_duration(timingArray[text])
                    .margin(right=textMovementsRight[text], left=textMovementsLeft[text], opacity=0))

        if checkEffect():
            txt_clip = fadein(txt_clip, 2, [255, 255, 0])
        else:
            txt_clip = fadeout(txt_clip, 2, [255, 255, 0])
        clip_list.append(txt_clip)

    final_clip = concatenate_videoclips(clip_list)
    return final_clip


def setAudio(fileName):
    audioclip = AudioFileClip(fileName)
    new_audioclip = CompositeAudioClip([audioclip])
    return new_audioclip


def returnLogo(fileName):
    logo = (ImageClip(fileName)
            .set_duration(30)
            .resize(height=50)  # if you need to resize..
            # (optional) logo-border padding
            .margin(right=50, top=50, opacity=0)
            .set_pos(("right", "top"))
            )
    logo.resize((100, 100))
    return logo

def previewVideo(fileName):
    logo = (ImageClip(fileName)
            .set_duration(10)
            .resize(height=540)  # if you need to resize..
            .set_pos(("center"))
            )
    logo.resize((540, 540))
    return logo

def assembleInputBasedVideo():

    if templateName in textMovements:
        if previewFlag:
            resizedVideo = resizeUserVideo(videoInput)
            maskedVideo = returnMaskedClip(templateName)
            previewedVideo = previewVideo(LOGO)
            result = CompositeVideoClip([resizedVideo, maskedVideo, setTextRL(templateName).set_start(
                returnSetStart(templateName)).set_position(("center", calculate_height(FONTSIZE))), previewedVideo])
            
        else:
            resizedVideo = resizeUserVideo(videoInput)
            maskedVideo = returnMaskedClip(templateName)
            logoVideo = returnLogo(LOGO)
            result = CompositeVideoClip([resizedVideo, maskedVideo, setTextRL(templateName).set_start(
                returnSetStart(templateName)).set_position(("center", calculate_height(FONTSIZE))), logoVideo])
    else:
        if previewFlag:
            resizedVideo = resizeUserVideo(videoInput)
            maskedVideo = returnMaskedClip(templateName)
            previewedVideo = previewVideo(LOGO)
            result = CompositeVideoClip([resizedVideo, maskedVideo, setText(templateName).set_start(
                returnSetStart(templateName)).set_position(("center", calculate_height(FONTSIZE))), previewedVideo])
        else:
            resizedVideo = resizeUserVideo(videoInput)
            maskedVideo = returnMaskedClip(templateName)
            logoVideo = returnLogo(LOGO)
            result = CompositeVideoClip([resizedVideo, maskedVideo, setText(templateName).set_start(
                returnSetStart(templateName)).set_position(("center", calculate_height(FONTSIZE))), logoVideo])

    return result

def composeVideo():
    result = assembleInputBasedVideo()
    result.audio = setAudio(audioClip)

    if previewFlag:
        result.set_duration(10).write_videofile(OUTPUT_FILE_NAME, fps=15, threads=THREADS*2, logger=None)
    else:
        result.set_duration(30).write_videofile(OUTPUT_FILE_NAME, fps=15, threads=THREADS*2, logger=None)

    if path.exists( OUTPUT_FILE_NAME ):
        shutil.move( "./" + OUTPUT_FILE_NAME, "./demoVideos" )
    

composeVideo()
