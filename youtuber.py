from pytube import YouTube
import os
import sys
from multiprocessing import Pipe


class GetNewVideo:
    messages = [
        "Um erro ocorreu ao tentar fazer o download:\n\t{sys.exc_info()}"
    ]
    def __init__(self, url:str, audio:bool|None=False, conn:Pipe=None) -> None:
        self.link = url
        self.optinal = audio
        self.source = YouTube(self.link)
        self.connection: Pipe = conn

        if audio:
            self.get_audio()
        else:
            self.get_video()
        
    def get_video(self):
        try:
            source = self.source.streams.get_lowest_resolution()
            filesize = source.filesize_kb
            self.connection.send(filesize)
            source.download()
            self.connection.send(True)
            self.connection.close()
            return
        except:
            print("eventErrorGET_video")
            self.connection.send(False)
            print(self.messages[0])
            raise ConnectionAbortedError
        
    def get_audio(self):
        try:
            source = self.source.streams.get_audio_only()
            filesize = source.filesize_kb
            self.connection.send(filesize)
            source.download()
            self.connection.send(True)
            self.connection.close()
            return
        except:
            print("eventErrorGET_audio")
            self.connection.send(False)
            print(self.messages[0])
            raise ConnectionAbortedError
    


if __name__ == "__main__":
    parent_conn, child_conn = Pipe()
    # https://youtube.com/shorts/E3sIC_g3F3Y?feature=share
    video = GetNewVideo("https://www.youtube.com/watch?v=Lo2qQmj0_h4", None, child_conn)
    video.get_video()
    while parent_conn.recv():
        print(parent_conn.recv())