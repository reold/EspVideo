from pytube import YouTube


class YoutubeHelper:
    def __init__(self):
        pass

    def download_video(self, url, path, name):

        try:
            yt = YouTube(url)
        except:
            print("Connection Error")

        # filters out all the files with "mp4" extension
        yt.streams.filter(progressive=True, file_extension="mp4").order_by(
            "resolution"
        ).desc().first().download(path, f"{name}.mp4")
