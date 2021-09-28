from moviepy.editor import VideoFileClip, VideoClip

video = VideoFileClip(r"downloads\video.mp4")

print(list(video.iter_frames()))
