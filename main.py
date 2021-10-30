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

    resized_video = video.resize(newsize=(64, 32))

    # resized_video.write_videofile("processed.mp4", fps=video.fps)

    normal_images = list(resized_video.iter_frames())
    low_fps_images = []
    bw_images = []


    # reduce video fps to 1

    if video.fps != 1:
        print(bcolors.OKGREEN + "- fps exceeds limit of 1, reducing frames")
        for frm_no, frame in enumerate(normal_images):
            if (frm_no % video.fps) == 0:
                low_fps_images.append(normal_images[frm_no])

    # convert image to grayscale
    # then append to list of black and white images


    print("- converting to black and white")

    for frame in low_fps_images:
        gray_image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        (thresh, bw_image) = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
        bw_images.append(bw_image)

    final_data = []

    print("- converting to usable information")
    for image in bw_images:
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
    json_object = str(final_data)

    # Writing to sample.json
    print("- writing data to file" + bcolors.ENDC)
    with open("processed_data.json", "w") as outfile:
        outfile.write(json_object)

elif job == "stream":
    import socket
    import json

    processed_data = NotImplemented

    with open("processed_data.json") as f:
        processed_data = json.load(f)

    print(f"{bcolors.OKGREEN}starting sockets server{bcolors.ENDC}")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind(("0.0.0.0", 80))
    server.listen(0)

    def send_data(client, frame, part):
        frame_data = processed_data[frame]
        if part == 0:
            frame_part = frame_data["data"][
                : int(len(frame_data["data"]) / 2) // 2 // 2 // 2 // 2 // 2
            ]
        elif part == 1:
            frame_part = frame_data["data"][
                int(len(frame_data["data"]) / 2)
                // 2
                // 2 : int(len(frame_data["data"]) / 2)
            ]
        else:
            pass

        client.send(str(frame_part).encode("utf-8"))

    while True:

        client, addr = server.accept()
        print(f"Connected by {addr}")

        stream_status = False
        old_frame = old_part = 0

        while True:
            cli_msg = client.recv(32).decode("UTF-8")

            if len(cli_msg) == 0:
                break
            else:
                if not stream_status:
                    if cli_msg == "START_STREAM":
                        stream_status = True
                        send_data(client, old_frame, old_part)
                elif stream_status:
                    if cli_msg == "NEXT_PART":
                        old_part += 1
                        send_data(client, old_frame, old_part)

                    if cli_msg.startswith("FRAME") == True:
                        old_frame = int(cli_msg[5:])
                        old_part = 0
                        send_data(client, old_frame, old_part)

        print("Closing connection")
        client.close()

else:
    print(bcolors.FAIL + "Invalid task name" + bcolors.ENDC)
