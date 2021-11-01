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
    from collections import Counter
    import json
    from imageProcessor import ImageProcessor

    image_processor = ImageProcessor()

    video = VideoFileClip(r"downloads\video.mp4")
    resized_video = video.resize(newsize=(64, 32))

    original_images = list(resized_video.iter_frames())
    low_fps_images = []
    black_white_images = []

    # reduce video fps to 1
    if video.fps != 1:
        print(bcolors.OKGREEN + "- fps exceeds limit of 1, reducing frames")
        for frm_no, frame in enumerate(original_images):
            if (frm_no % video.fps) == 0:
                low_fps_images.append(original_images[frm_no])

    # convert image to grayscale
    # then append to list of black and white images

    print("- converting to black and white")

    for frame in low_fps_images:
        processed_image = image_processor.process_image(frame)
        black_white_images.append(processed_image)

    final_data = []
    print("- converting to usable information")

    for image in black_white_images:
        final_data.append({})

        black_amount = white_amount = 0

        for row in image.tolist():
            for color in image:
                color_amount = Counter(color)

                black_amount += color_amount[0]
                white_amount += color_amount[255]

        print(black_amount)
        print(white_amount)

        if black_amount >= white_amount:
            # black data is more, so save white data
            final_data[-1]["whitedata"] = True
            final_data[-1]["data"] = []

        elif white_amount >= black_amount:
            final_data[-1]["whitedata"] = True
            final_data[-1]["data"] = []

        for no_row, row in enumerate(image.tolist()):
            for no_pixel, pixel in enumerate(row):
                if black_amount >= white_amount:
                    # black data is more, save white data
                    if pixel == 255:
                        final_data[-1]["data"].append({"x": no_pixel, "y": no_row})
                elif white_amount >= black_amount:

                    if pixel == 0:
                        final_data[-1]["data"].append({"x": no_pixel, "y": no_row})

    # for image in black_white_images:
    #     final_data.append({})
    #     black_amount = white_amount = 0
    #     for row_no, row in enumerate(image):
    #         for pixel_no, pixel in enumerate(image):
    #             if pixel == (0, 0, 0):
    #                 black_amount += 1
    #             elif pixel == (255, 255, 255):
    #                 white_amount += 1

    #     if black_amount >= white_amount:
    #         final_data[len(final_data) - 1]["whitedata"] = True
    #         final_data[len(final_data) - 1]["data"] = []

    #         for row_no, row in enumerate(image):
    #             for pixel_no, pixel in enumerate(row):
    #                 if pixel == 0:
    #                     final_data[len(final_data) - 1]["data"].append(
    #                         {"x": pixel_no, "y": row_no}
    #                     )
    #     if black_amount <= white_amount:
    #         final_data[len(final_data) - 1]["whitedata"] = False
    #         final_data[len(final_data) - 1]["data"] = []

    #         for row_no, row in enumerate(image):
    #             for pixel_no, pixel in enumerate(row):
    #                 if pixel == 255:
    #                     final_data[len(final_data) - 1]["data"].append(
    #                         {"x": pixel_no, "y": row_no}
    #                     )

    print(f"- total frames: {len(final_data)}")

    # Serializing json
    json_object = json.dumps(final_data)

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

    class ClientUtils:
        def __init__(self, client, addr):
            self.client = client
            self.addr = addr

        def getFrameData(self, params):

            frame_no, frame_part = params

            frame_no = int(frame_no)
            frame_part = int(frame_part)

            print(params)

            # frame_no, frame_part = int(frame_no), int(frame_part)

            print(f"fetching frame {frame_no} data")

            frame_data = processed_data[int(frame_no)]
            frame_part_data = {"whitedata": frame_data["whitedata"]}
            frame_part_data["data"] = frame_data["data"][
                int(frame_part) : (int(frame_part) + 10)
            ]

            print(frame_part_data)

            client.send(json.dumps(frame_part_data).encode("utf-8"))

        def noPixels(self, params):

            frame_no = params[0]

            frame_no = int(frame_no)

            client.send(str(len(processed_data[frame_no]["data"])).encode("utf-8"))

    while True:
        client, addr = server.accept()
        client_utils = ClientUtils(client, addr)
        print(f"connected by {addr}")

        while True:
            client_msg = client.recv(64).decode("utf-8")

            print(f"client message: {client_msg}")

            if client_msg.startswith("getFrameData"):
                params = client_msg.split(",")[1:]
                client_utils.getFrameData(params)

            elif client_msg.startswith("noPixels"):
                params = client_msg.split(",")[1:]
                client_utils.noPixels(params)

            if client_msg == "!quit" or len(client_msg) == 0:
                print("client quit")
                break

        client.close()


else:
    print(bcolors.FAIL + "Invalid task name" + bcolors.ENDC)
