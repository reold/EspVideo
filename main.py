import sys
import os
from typing import final
from youtubeHelper import YoutubeHelper

yt_helper = YoutubeHelper()


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


try:
    job = sys.argv[1]
    os.system("cls")
    print(
        f"{bcolors.OKCYAN}Task:{bcolors.ENDC} {bcolors.UNDERLINE}{job}{bcolors.ENDC}",
        end="\n\n",
    )
except:
    print(bcolors.BOLD + bcolors.FAIL + "no argument/s passed" + bcolors.ENDC)
    exit()

if job == "download":

    try:
        url = sys.argv[2]
        print(f"{bcolors.OKGREEN}url: {url}{bcolors.ENDC}")
    except:
        print(bcolors.FAIL + "url not passed" + bcolors.ENDC)
        exit()

    print(bcolors.OKGREEN + "Video downloading", end="")
    yt_helper.download_video(url, "downloads", "video")
    print(" done!" + bcolors.ENDC)

elif job == "process":
    from moviepy.editor import VideoFileClip
    import cv2
    import json

    final_video_frames = []

    video = VideoFileClip(r"downloads\video.mp4")

    resized_video = video.resize(newsize=(128, 64))

    # resized_video.write_videofile("processed.mp4", fps=video.fps)

    bw_images = []

    # convert image to grayscale
    # then append to list of black and white images
    print(bcolors.OKGREEN + "- converting to black and white")
    for frame in resized_video.iter_frames():
        gray_image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        (thresh, bw_image) = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
        bw_images.append(bw_image)

    final_images = []

    if video.fps != 1:
        print("- fps exceeds limit of 1, reducing frames")
        for frm_no, frame in enumerate(bw_images):
            if (frm_no % video.fps) == 0:
                final_images.append(bw_images[frm_no])

    final_data = []

    print("- converting to usable information")
    for image in final_images:
        final_data.append({})
        black_amount = white_amount = 0
        for row_no, row in enumerate(image):
            for pixel_no, pixel in enumerate(image):
                if pixel == (0, 0, 0):
                    black_amount += 1
                elif pixel == (255, 255, 255):
                    white_amount += 1

        if black_amount >= white_amount:
            final_data[len(final_data) - 1]["whitedata"] = True
            final_data[len(final_data) - 1]["data"] = []

            for row_no, row in enumerate(image):
                for pixel_no, pixel in enumerate(row):
                    if pixel == 0:
                        final_data[len(final_data) - 1]["data"].append(
                            {"x": pixel_no, "y": row_no}
                        )
        if black_amount <= white_amount:
            final_data[len(final_data) - 1]["whitedata"] = False
            final_data[len(final_data) - 1]["data"] = []

            for row_no, row in enumerate(image):
                for pixel_no, pixel in enumerate(row):
                    if pixel == 255:
                        final_data[len(final_data) - 1]["data"].append(
                            {"x": pixel_no, "y": row_no}
                        )

    print(f"- total frames: {len(final_data)}")

    # Serializing json
    json_object = json.dumps(final_data, indent=4)

    # Writing to sample.json
    print("- writing data to file" + bcolors.ENDC)
    with open("processed_data.json", "w") as outfile:
        outfile.write(json_object)


else:
    print(bcolors.FAIL + "Invalid task name" + bcolors.ENDC)
