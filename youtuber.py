from pytube import YouTube
import os
import sys
from multiprocessing import Pipe
from threading import Thread, ThreadError


class GetNewVideo:
    
    def __init__(self, url:str, audio:bool|None=None, download:bool|None=True, conn:Pipe=None) -> None:
        self.link = url
        self.optinal = audio
        self.source = YouTube(self.link)
        self.connection: Pipe = conn

        if download:
            if audio:
                self.get_audio()
            else: self.get_video()
        

    def get_video(self):
        
        source = self.source.streams.get_lowest_resolution()
        print(f"Tamanho do video: {float(source.filesize_kb):.2f}kb")
        self.connection.send(f"CONN: Baixando Video: {source.title}")
        self.connection.send(f"CONN: Tamanho do video: {float(source.filesize_kb):.2f}kb")
        try:
            source.download()
            self.connection.send("Download Concluído")
            self.connection.close()
        except:
            print(f"Um erro ocorreu ao tentar fazer o download: \n\t{sys.exc_info()}")

        
            
    def get_audio(self):
        self.source.streams.get_lowest_resolution().download()
    

    def get_filesize(self):
        source = self.source.streams.get_lowest_resolution()
        return f"{float(source.filesize/1024):.2f}kb"



if __name__ == "__main__":
    # https://youtube.com/shorts/E3sIC_g3F3Y?feature=share
    video = GetNewVideo("https://www.youtube.com/watch?v=Lo2qQmj0_h4")
    video.get_video()