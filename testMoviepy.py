from moviepy.editor import *

# video2 = VideoFileClip("newTemplate.webM", audio=False)
# video1 = VideoFileClip("newtempVideo.mp4", audio=False).subclip(0, 30)
# video2 = VideoFileClip("newTemplate.webM", audio=False).set_opacity(0.9).resize(( 320, 240 ))
# video2.show(10, interactive=True)
# w1, h1 = video1.size
# w2, h2 = video2.size
# print(w1, h1, w2, h2)

# video2 = VideoFileClip("newVideo.webM").resize((w/3, h/3)).set_opacity(.70)
# masked_clip = video2.fx(vfx.mask_color, color=[71, 226, 211], thr=100, s=5)
# # video.write_videofile("test.mp4",fps=25)

# # # w2, h2 = video2.size
# txt_clip = (TextClip("Hello World!", fontsize=50, color='white')
#             .set_position((364, 873))
#             .set_duration(15))

text_list = ["Piggy", "Kermit", "Gonzo", "Fozzie"]
clip_list = []
txt_clip = TextClip(" ", fontsize=50, color='white').set_duration(
    5).set_position((364, 873))
clip_list.append(txt_clip)

for text in text_list:
    try:
        txt_clip = TextClip(text, fontsize=50, color='white').set_duration(
            5).set_position((364, 873))
        clip_list.append(txt_clip)
    except UnicodeEncodeError:

        txt_clip = TextClip("Issue with text", fontsize=50, color='white').set_duration(
            2).set_position((364, 873))
        clip_list.append(txt_clip)

# txt_col = txt_clip.on_color(size=( 100, 100 ),
#                   color=(0,0,0), pos=(6,'center'), col_opacity=0.6)

# txt_mov = txt_col.set_pos( lambda t: (max(w1/30,int(w1-0.5*w1*t)),
#                                   max(5*h1/6,int(100*t))) )
final_clip = concatenate_videoclips(clip_list)
video = VideoFileClip("finalVideo.mp4")
result = CompositeVideoClip([video, final_clip.set_position((443, 880))])
# result.set_duration = 30
# audioclip = AudioFileClip("test.mp3")
# new_audioclip = CompositeAudioClip([audioclip])
# # # adding audio to the video clip
# result.audio = new_audioclip
# result.show(10, interactive=True)
# result.show(10, interactive=True)
result.write_videofile("output.mp4", fps=25)

# # loading audio file

# concat = concatenate_audioclips([aclip1, aclip2, aclip3])
# compo = CompositeAudioClip([aclip1.volumex(1.2),
#                             aclip2.set_start(5), # start at t=5s
#                             aclip3.set_start(9)])
