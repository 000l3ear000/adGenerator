from moviepy.editor import *
from moviepy.video import *

HEIGHT = 615
FONTSIZE = 50


def calculate_height(fontSize):
    return HEIGHT - (fontSize / 2)


# video2 = VideoFileClip("newTemplate.webM", audio=False)
video1 = VideoFileClip("greenTemplate.webM", audio=False)
# video2 = VideoFileClip("newTemplate.webM", audio=False)
video2 = VideoFileClip("video1.mp4", audio=False).resize((720, 720))
# video1.show(10, interactive=True)
# w1, h1 = video1.size
# w2, h2 = video2.size
# print(w1, h1, w2, h2)

# video2 = VideoFileClip("newVideo.webM").resize((w/3, h/3)).set_opacity(.70)
# masked_clip = video2.fx(vfx.mask_color, color=[71, 226, 211], thr=100, s=5)
masked_clip = video1.fx(vfx.mask_color, color=[82, 254, 238], thr=100, s=5)
# masked_clip = video2.fx.loop( n = 5 )
# # video.write_videofile("test.mp4",fps=25)

# # # w2, h2 = video2.size
# txt_clip = (TextClip("Hello World!", fontsize=50, color='white')
#             .set_position((364, 873))
#             .set_duration(15))

# 4.5
# 6

text_list = ["Gonzo", "Fozzie"]
clip_list = []
txt_clip = TextClip("Piggy", fontsize=FONTSIZE,
                    color='white').set_duration(3.8)
clip_list.append(txt_clip)
txt_clip = TextClip("Hello World!", fontsize=FONTSIZE,
                    color='white').set_duration(4.6)
clip_list.append(txt_clip)
txt_clip = TextClip("Kermit!", fontsize=FONTSIZE,
                    color='white').set_duration(6)
clip_list.append(txt_clip)

for text in text_list:
    try:
        txt_clip = TextClip(text, fontsize=FONTSIZE,
                            color='white').set_duration(6.5)
        clip_list.append(txt_clip)
    except UnicodeEncodeError:

        txt_clip = TextClip("Issue with text", fontsize=FONTSIZE,
                            color='white').set_duration(5)
        clip_list.append(txt_clip)

# txt_col = txt_clip.on_color(size=( 100, 100 ),
#                   color=(0,0,0), pos=(6,'center'), col_opacity=0.6)

# txt_mov = txt_col.set_pos( lambda t: (max(w1/30,int(w1-0.5*w1*t)),
#                                   max(5*h1/6,int(100*t))) )
video = VideoFileClip("finalVideo3.mp4")
final_clip = concatenate_videoclips(clip_list)
# video.show(10, interactive=True)
# result = CompositeVideoClip([video, final_clip.set_start(1).set_position(("center", calculate_height(FONTSIZE)))])
result = CompositeVideoClip([video2, masked_clip.set_opacity(.7), final_clip.set_start(
    1).set_position(("center", calculate_height(FONTSIZE)))])
# result = CompositeVideoClip([video1])
# result.set_duration = 10
audioclip = AudioFileClip("test.mp3")
new_audioclip = CompositeAudioClip([audioclip])
# # adding audio to the video clip
result.audio = new_audioclip
# result.show(10, interactive=True)
# result.show(10, interactive=True)
result.write_videofile("finalVideo6.mp4", fps=30)

# # loading audio file

# concat = concatenate_audioclips([aclip1, aclip2, aclip3])
# compo = CompositeAudioClip([aclip1.volumex(1.2),
#                             aclip2.set_start(5), # start at t=5s
#                             aclip3.set_start(9)])
