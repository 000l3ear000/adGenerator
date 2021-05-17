from sys import argv
from os import path, remove
from moviepy.video.io.ffmpeg_tools import ffmpeg_resize
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeAudioClip, CompositeVideoClip, concatenate_videoclips, ImageClip
from moviepy.video.fx.mask_color import mask_color
from moviepy.video.fx.all import fadein, fadeout
from math import ceil
import shutil

HEIGHT = 920
FONTSIZE = 70
FONTCOLOR = "white"
FONTEFFECT = "fadeout"
RESIZED_VIDEO = "resized.mp4"
FRAME_FILENAME = "framePreview.png"
LOGO = "logo.png"

# Template_16.webM "Text 1","Text 2","Text 3","Text 4","Text 5" video1.mp4 Cute.mp3 "50","green","fadeout"
epicDict = {
    "Template_1.webM": [[4.8, 4.8, 6, 6, 3.5], 1, [81, 253, 234], 920],
    "Template_2.webM": [[4.8, 4.8, 6, 6, 3.5], 1, [81, 253, 234], 920],

    "Template_3.webM": [[3.8, 4.6, 6, 6.6, 6], 1, [80, 252, 236], 960],
    "Template_4.webM": [[3.8, 4.6, 6, 6.6, 6], 1, [80, 252, 236], 960],

    "Template_5.webM": [[4.5, 6, 6, 4], 4.8, [71, 226, 211], 920],
    "Template_6.webM": [[4.5, 6, 6, 4], 4.8, [71, 226, 211], 920],

    "Template_7.webM": [[4.8, 4.8, 6, 6, 6.2], 0, [82, 254, 238], 930],
    "Template_8.webM": [[4.8, 4.8, 6, 6, 6.2], 0, [82, 254, 238], 930],

    "Template_9.webM": [[4.8, 4.8, 6, 6, 6.2], 0, [80, 252, 236], 930],
    "Template_10.webM": [[4.8, 4.8, 6, 6, 6.2], 0, [80, 252, 236], 930],

    "Template_11.webM": [[4.8, 4.8, 6, 6, 6.2], 0, [80, 252, 236], 930],
    "Template_12.webM": [[4.5, 6, 6, 6], 3.8, [80, 252, 236], 930],

    "Template_13.webM": [[3.8, 4.6, 6, 6.6, 6.5], 1, [80, 252, 236], 960],
    "Template_14.webM": [[3.8, 4.6, 6, 6.6, 6.5], 1, [80, 252, 236], 960],

    "Template_15.webM": [[3.8, 4.6, 6, 6.6, 6.6], 1, [80, 252, 236], 960],
    "Template_16.webM": [[3.8, 4.6, 6, 6.6, 6.6], 1, [80, 252, 236], 960],

    "Template_17.webM": [[3.8, 4.6, 6, 6.6, 6.6], 1, [80, 252, 236], 960],
    "Template_18.webM": [[3.8, 4.6, 6, 6.6, 6.6], 1, [80, 252, 236], 960],

    "Template_19.webM": [[3.8, 4.6, 6, 6.6, 6.5], 1, [80, 252, 236], 960],
    "Template_20.webM": [[3.8, 4.6, 6, 6.6, 6.5], 1, [80, 252, 236], 960]
}

textMovements = ['Template_7.webM', 'Template_8.webM',
                 'Template_9.webM', 'Template_10.webM']
textMovementsRight = [200, 0, 200, 0, 200]
textMovementsLeft = [0, 200, 0, 200, 0]
videoFormats = ['mp4', 'webM', 'mov', 'mpeg-4', 'flv', 'avi', 'mkv', 'wmv']
imageFormats = ['jpeg', 'png', 'jpg', 'svg']

# print(argv)
if argv.__len__() > 5:

    templateName = argv[1]
    textArray = argv[2].split(',')
    videoInput = argv[3]
    audioClip = argv[4]
    fontProperties = argv[5].split(',')
    fontSize = int(fontProperties[0])
    fontColor = fontProperties[1]
    fontEffect = fontProperties[2]
    fontStyle = fontProperties[3]
    OUTPUT_FILE_NAME = fontProperties[4]
    previewFlag = argv[6] if argv.__len__() == 7 else 0

    print(fontSize, fontColor, fontEffect, fontStyle, OUTPUT_FILE_NAME, previewFlag)
    print(templateName, textArray[0], videoInput, audioClip)


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

        if path.exists(RESIZED_VIDEO):
            remove(RESIZED_VIDEO)

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
            return VideoFileClip(RESIZED_VIDEO, audio=False).subclip(0, 10)
        else:
            return VideoFileClip(RESIZED_VIDEO, audio=False)

        # return resizedVideo
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
            result = CompositeVideoClip([resizeUserVideo(videoInput), returnMaskedClip(templateName), setTextRL(templateName).set_start(
                returnSetStart(templateName)).set_position(("center", calculate_height(FONTSIZE))), previewVideo(LOGO)])
        else:
            result = CompositeVideoClip([resizeUserVideo(videoInput), returnMaskedClip(templateName), setTextRL(templateName).set_start(
                returnSetStart(templateName)).set_position(("center", calculate_height(FONTSIZE))), returnLogo(LOGO)])
    else:
        if previewFlag:
            result = CompositeVideoClip([resizeUserVideo(videoInput), returnMaskedClip(templateName), setText(templateName).set_start(
                returnSetStart(templateName)).set_position(("center", calculate_height(FONTSIZE))), previewVideo(LOGO)])
        else:
            result = CompositeVideoClip([resizeUserVideo(videoInput), returnMaskedClip(templateName), setText(templateName).set_start(
                returnSetStart(templateName)).set_position(("center", calculate_height(FONTSIZE))), returnLogo(LOGO)])
    
    return result


def composeVideo():
    result = assembleInputBasedVideo()
    result.audio = setAudio(audioClip)

    if previewFlag:
        result.set_duration(10).write_videofile(OUTPUT_FILE_NAME, fps=24, threads=8, logger=None)
    else:
        result.set_duration(30).write_videofile(OUTPUT_FILE_NAME, fps=24, threads=8, logger=None)

    if path.exists( OUTPUT_FILE_NAME ):
        shutil.move( "./" + OUTPUT_FILE_NAME, "./demoVideos" )


composeVideo()