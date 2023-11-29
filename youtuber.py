from pytube import YouTube
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

        #if audio:
        #    self.get_audio()
        #else:
        #    self.get_video()
    
    def get_viedeo_res(self) -> list:
        try:
            data = {"data": self.source.streaming_data, "thumb":self.source.thumbnail_url, "id":self.source.video_id}
            
            #for video in data["formats"]:
            #    print(video["qualityLabel"])
            return data
            
        except:
            print("eventErrorGET_video")
            self.connection.send(False)
            print(self.messages[0])
            self.connection.close()
            raise ConnectionAbortedError
        
    def get_video(self):
        try:
            source = self.source.streams.get_highest_resolution()
            filesize = source.filesize_kb
            print(f"Tamanho do video: {filesize}")
            self.connection.send(filesize)
            source.download()
            self.connection.send(True)
            self.connection.close()
            return
        except:
            print("eventErrorGET_video")
            self.connection.send(False)
            print(self.messages[0])
            self.connection.close()
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
    data = video.get_viedeo_res()
    # while parent_conn.recv():
    #    print(parent_conn.recv())
    