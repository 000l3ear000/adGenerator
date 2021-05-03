from sys import argv
from os import path, remove
from moviepy.video.io.ffmpeg_tools import ffmpeg_resize
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeAudioClip, CompositeVideoClip, concatenate_videoclips, ImageClip
from moviepy.video.fx.mask_color import mask_color
from moviepy.video.fx.all import fadein, fadeout
import pyrebase
# from moviepy.video import *

HEIGHT = 920
FONTSIZE = 70
FONTCOLOR = "white"
FONTEFFECT = "fadeout"
OUTPUT_FILE_NAME = "ad.mp4"
RESIZED_VIDEO = "resized.mp4"
FRAME_FILENAME = "framePreview.png"
LOGO = "logo.png"



config = {
    "apiKey": "AIzaSyDvYb9sgl85AgyTriAgHwLg_-uadcFXlWY",
    "authDomain": "imagepreview-aef2b.firebaseapp.com",
    "projectId": "imagepreview-aef2b",
    "databaseURL": "https://imagepreview-aef2b.firebaseio.com",
    "storageBucket": "imagepreview-aef2b.appspot.com",
    "messagingSenderId": "46502678413",
    "appId": "1:46502678413:web:650b751df6da56d46577c4",
    "measurementId": "G-W7KEVXRSG2"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
email = "testuser@gmail.com"
password = "123456"

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
                 'Template_9.webM', 'Template_70.webM']
textMovementsRight = [200, 0, 200, 0, 200]
textMovementsLeft = [0, 200, 0, 200, 0]
videoFormats = ['mp4', 'webM', 'mov', 'mpeg-4', 'flv', 'avi', 'mkv', 'wmv']
imageFormats = ['jpeg', 'png', 'jpg', 'svg']

if argv.__len__() > 6:

    print("5 args found")
    print(argv)
    # splitTemplateName = argv[1].split('.')
    templateName = argv[1]
    textArray = argv[2].split(',')
    videoInput = argv[3]
    print(videoInput)
    audioClip = argv[4]
    fontProperties = argv[5].split(',')
    fontSize = int(fontProperties[0])
    fontColor = fontProperties[1]
    fontEffect = "fadeout" if fontProperties.__len__(
    ) == 3 else fontProperties[2]
    fontStyle = fontProperties[3] if fontProperties.__len__(
    ) == 4 else fontProperties[2]
    saveFrame = argv[6].split(',')
    saveFrameFlag = saveFrame[0]
    saveFrameTime = int(saveFrame[1])
    print(templateName, textArray, videoInput, audioClip)


def saveFrame():
    getResult = composeVideo()
    getResult.save_frame( FRAME_FILENAME, t = saveFrameTime )

def getImageUrl():
    auth = firebase.auth()
    # userCreated = auth.create_user_with_email_and_password(email, password)
    user = auth.sign_in_with_email_and_password(email, password)
    url = storage.child(FRAME_FILENAME).get_url(user['idToken'])
    print(url)

def uploadPreviewImage():
    saveFrame()
    storage.child(FRAME_FILENAME).put(FRAME_FILENAME)
    getImageUrl()

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


def resizeUserVideo(userVid):
    if checkInputFile(userVid) == 1:
        # resizedVideo = VideoFileClip( userVid, audio=False).resize(( 1080, 1080 ))
        if path.exists(RESIZED_VIDEO):
            remove(RESIZED_VIDEO)

        ffmpeg_resize(userVid, RESIZED_VIDEO, [1080, 1080])
        return VideoFileClip(RESIZED_VIDEO, audio=False)

        # return resizedVideo
    elif checkInputFile(userVid) == 2:
        return ImageClip(userVid).resize((1080, 1080)).set_duration(30)
    else:
        return "unknown file uploaded"


def returnMaskedClip(fileName):
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
        txt_clip = TextClip(textArray[text], fontsize=fontSize, font=fontStyle,
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

        # marginValue = textMovementsRight[text]
        # print(marginValue)
        # slicing the array to exlude double quotes
        txt_clip = (TextClip(textArray[text], fontsize=fontSize, font=fontStyle,
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


def composeVideo():
    # resizedVideo = resizeUserVideo( videoInput )
    # resizedVideo.close()
    # remove(RESIZED_VIDEO)
    if templateName in textMovements:
        result = CompositeVideoClip([resizeUserVideo(videoInput), returnMaskedClip(templateName), setTextRL(templateName).set_start(
            returnSetStart(templateName)).set_position(("center", calculate_height(FONTSIZE))), returnLogo(LOGO)])
    else:
        result = CompositeVideoClip([resizeUserVideo(videoInput), returnMaskedClip(templateName), setText(templateName).set_start(
            returnSetStart(templateName)).set_position(("center", calculate_height(FONTSIZE))), returnLogo(LOGO)])
    # result.show(10, interactive=True)
    # result.set_duration(10)
    # lst = TextClip.list('font')
    # print(lst)
    if saveFrameFlag == "true":
        return result
    # result.audio = setAudio(audioClip)
    # result.write_videofile(OUTPUT_FILE_NAME, fps=24, threads=8)


# composeVideo()
uploadPreviewImage()
# print(checkInputFile(videoInput))

# vid = VideoFileClip("Templates/Export templates/Template 20.mov")
# vid = VideoFileClip("Template_3.webM")
# res = CompositeVideoClip([vid])
# res.show(10, interactive=True)
# res.write_videofile("Template_20.webM", fps = 24)
# except UniodeEncodeError:
#     txt_clip = TextClip("Issue with text", fontsize=FONTSIZE,
#                         color='white').set_duration(5)
#     clip_list.append(txt_clip)

# video2 = VideoFileClip("newTemplate.webM", audio=False)
# video1 = VideoFileClip(
#     "Template 6/newTemplate.webM", audio=False).resize(( 1080, 1080 ))
# video1 = VideoFileClip( "newTemplate2.webM" )
# video2 = VideoFileClip("newTemplate.webM", audio=False)
# video2 = VideoFileClip("sampleVideo.mp4", audio=False)
# video1.show(10, interactive=True)
# w1, h1 = video1.size
# print(w1, h1)
# w2, h2 = video2.size
# print(w1, h1, w2, h2)

# masked_clip = mask_color(video1, color=[71, 226, 211], thr=100, s=5)

# video2 = VideoFileClip("newVideo.webM").resize((w/3, h/3)).set_opacity(.70)
# masked_clip = video2.fx(vfx.mask_color, color=[71, 226, 211], thr=100, s=5)
#  = video1.mask_color(color=[82, 254, 238], thr=100, s=5)
# masked_clip = video2.fx.loop( n = 5 )
# # video.write_videofile("test.mp4",fps=25)

# # # w2, h2 = video2.size
# txt_clip = (TextClip("Hello World!", fontsize=50, color='white')
#             .set_position((364, 873))
#             .set_duration(15))

# 4.5
# 6

# text_list = ["Kermit", "Gonzo", "Fozzie"]
# clip_list = []
# txt_clip = TextClip("Piggy", fontsize=FONTSIZE,
#                     color='white').set_duration(4.5)
# clip_list.append(txt_clip)
# # txt_clip = TextClip("Hello World!", fontsize=FONTSIZE,
# #                     color='white').set_duration(4.6)
# # clip_list.append(txt_clip)
# # txt_clip = TextClip("Kermit!", fontsize=FONTSIZE,
# #                     color='white').set_duration(6)
# # clip_list.append(txt_clip)

# for text in text_list:
#     try:
#         txt_clip = TextClip(text, fontsize=FONTSIZE,
#                             color='white').set_duration(6)
#         clip_list.append(txt_clip)
#     except UnicodeEncodeError:

#         txt_clip = TextClip("Issue with text", fontsize=FONTSIZE,
#                             color='white').set_duration(5)
#         clip_list.append(txt_clip)

# txt_col = txt_clip.on_color(size=( 100, 100 ),
#                   color=(0,0,0), pos=(6,'center'), col_opacity=0.6)

# txt_mov = txt_col.set_pos( lambda t: (max(w1/30,int(w1-0.5*w1*t)),
#                                   max(5*h1/6,int(100*t))) )
# video = VideoFileClip("finalVideo3.mp4")
# final_clip = concatenate_videoclips(clip_list)
# video.show(10, interactive=True)
# result = CompositeVideoClip([video, final_clip.set_start(1).set_position(("center", calculate_height(FONTSIZE)))])
# result = CompositeVideoClip([video2, masked_clip.set_opacity(.7), final_clip.set_start(
# 5).set_position(("center", calculate_height(FONTSIZE)))])
# result = CompositeVideoClip([video1])
# result.set_duration = 10
# audioclip = AudioFileClip("Templates/Export Music/Cute.mp3")
# new_audioclip = CompositeAudioClip([audioclip])
# adding audio to the video clip
# result.audio = new_audioclip
# result.show(20, interactive=True)
# result.show(10, interactive=True)
# result.write_videofile("output2.mp4", fps=30)

# # loading audio file

# concat = concatenate_audioclips([aclip1, aclip2, aclip3])
# compo = CompositeAudioClip([aclip1.volumex(1.2),
#                             aclip2.set_start(5), # start at t=5s
#                             aclip3.set_start(9)])
