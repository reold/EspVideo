import sys
from typing import final
from youtubeHelper import YoutubeHelper

yt_helper = YoutubeHelper()

try:
    job = sys.argv[1]
    print(f"Task: {job}")
except:
    print("no argument/s passed")
    exit()

if job == "download":

    try:
        url = sys.argv[2]
        print(f"Url: {url}")
    except:
        print("url not passed")
        exit()

    print("Video downloading", end="")
    yt_helper.download_video(url, "downloads", "video")
    print(" done!")

elif job == "process":
    from moviepy.editor import VideoFileClip
    import cv2

    final_video_frames = []

    video = VideoFileClip(r"downloads\video.mp4")

    resized_video = video.resize(newsize=(128, 64))

    # resized_video.write_videofile("processed.mp4", fps=video.fps)

    bw_images = []

    for frame in resized_video.iter_frames():
        gray_image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        (thresh, bw_image) = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
        bw_images.append(bw_image)

    final_images = bw_images

    for image in final_images:
        for row_no, row in enumerate(image):
            for pixel_no, pixel in enumerate(image):
                final_images[row_no][pixel_no] = 0 if pixel == (0, 0, 0) else 1

    print(final_images)

else:
    print("Invalid task name")
