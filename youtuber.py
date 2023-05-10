from pytube import YouTube
import os
import sys
from multiprocessing import Pipe
from threading import Thread, ThreadError


class GetNewVideo:

    def __init__(
            self, url:str, audio:bool|None=None, 
            download:bool|None=True, 
            conn:Pipe=None
    ) -> None:
        self.link = url
        self.optinal = audio
        self.source = YouTube(self.link)
        
        self.connection: Pipe = conn
        
        if download:
            if audio:
                self.get_audio()
            else:
                try:
                    self.source.check_availability()
                    self.get_video()
                except:
                    print(sys.exc_info())
                    self.connection.send(False)
                    return
        
    def get_video(self):
        print("Get_Video")
        source = self.source.streams.get_lowest_resolution()
        filesize = source.filesize_kb
        
        if source != None:
            self.connection.send(filesize)
            print(f"eventSendTRUE | Filesize: {filesize}")
        else:
            print("eventSendNONE")
            self.connection.send(None)
            print("eventClosed")
            raise ConnectionAbortedError
            
        
        try:
            print("eventDownloadStart")
            source.download()
            print("eventDownloadFinish")
            self.connection.send(True)
            self.connection.close()
        except:
            print("eventErrorDownload")
            self.connection.send(False)
            print(f"Um erro ocorreu ao tentar fazer o download:\n\t{sys.exc_info()}")
            raise ConnectionAbortedError
            
    def get_audio(self):
        self.source.streams.get_audio_only.download()
    


if __name__ == "__main__":
    parent_conn, child_conn = Pipe()
    # https://youtube.com/shorts/E3sIC_g3F3Y?feature=share
    video = GetNewVideo("https://www.youtube.com/watch?v=Lo2qQmj0_h4", None, True, child_conn)
    video.get_video()
    while parent_conn.recv():
        print(parent_conn.recv())