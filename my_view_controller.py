from tkinter import Frame, Label, Button, PhotoImage
from GetThumbs import GetThumb
import threading
import youtuber
import os
import sys 
from multiprocessing import Pipe
from PIL import ImageTk, Image
from View import MyView

class MyViewController(MyView):
    def __init__(self, root) -> None:
        super().__init__(root)

    def build_view(self, values:list):
        viewFrame = Frame(self.internal_frame)
        for count, item in enumerate(values):
            tempFrame = Frame(viewFrame, relief="ridge", bd=2)
            
            self.config_data_playList(item, count, tempFrame)
            self.request_thumb(item, count)
            
            # Configurando a posicao do frame de widgets na visualizacao
            tempFrame.pack(expand=1, fill="x",
                ipadx=4, ipady=4, padx=2, pady=2, anchor="center")
            
        # Adicionando a visualizacao ao frame principal
        viewFrame.pack(expand=True, fill="both",
            ipadx=4, ipady=4, padx=2, pady=2, anchor="center")
        
        
    def config_data_playList(self, item, indexer:int, root):
        
        video_id=item["snippet"]["resourceId"]["videoId"]
        # Configurando as propriedades da visualizacao dos dados
        self.widgets.update({
            f"image{indexer}": Label(root, text=f"image{indexer}", image=self.not_found, anchor="sw"),
            f"text{indexer}": Label( root, text=f'{item["snippet"]["title"]}', anchor="sw"),
            f"descT{indexer}": Label(root, text=f'Canal: {item["snippet"]["channelTitle"]}', anchor="sw"),
            f"descD{indexer}": Label(root, text=f'Data: {item["snippet"]["publishedAt"]}', anchor="sw"),
            f"descId{indexer}": Label(root, text=f'vId: {item["snippet"]["resourceId"]["videoId"]}', anchor="sw"),
            f"button{indexer}": Button( # Configurando o botao e a configuracao de funcionalidade
                root, text="Download Video", relief="flat", bg="cyan", anchor="center",
                command=lambda id=video_id, btt=indexer: 
                threading.Thread(target=self.download, args=(id, btt)).start()),
            f"button_audio{indexer}": Button( # Configurando o botao e a configuracao de funcionalidade
                root, text="Download Audio", relief="flat", bg="yellow", anchor="center",
                command=lambda id=video_id, btt=f"_audio{indexer}": 
                threading.Thread(target=self.download, args=(id, btt, True)).start())})
    
    
    def request_thumb(self, item, indexer) -> bool:
        try: # Lancando uma requisicao em segundo plano para obter a thumbnail do video 
                target = self.widgets[f"image{indexer}"]
                url = item["snippet"]["thumbnails"]["default"]["url"]
                _id = item["snippet"]["resourceId"]["videoId"]
                thread = threading.Thread(target=self.get_thumb, args=(target, url, _id))
                thread.start()
        except KeyError:
            # Caso o video estiver indisponivel ou deletado, a thumb nao sera baixada.
            return False
        
    def show_view(self):
        for key, widget in self.widgets.items():
            target:Label|Button = widget
            if "image" in key:
                target.pack(side="left", expand=False, ipadx=1, ipady=1, padx=1, pady=1)
                self.internal_frame.update_idletasks()
            elif "text" in key:
                target.pack(expand=False, fill="x", ipadx=1, ipady=1, padx=1, pady=1)
            elif "desc" in key:
                target.pack(expand=False, fill="x", ipadx=1, ipady=1, padx=1, pady=1)
            elif "button" in key:
                target.pack(side="left", expand=False, fill="x", ipadx=2, ipady=2, padx=2, pady=2)

    def get_thumb(self, target:Label, url:str, id):

        if os.path.exists(f"{os.path.dirname(__file__)}\\thumbs\\thumb{id}.jpg"):
            self.set_image(target, id)
        else:
            thumb = GetThumb(url, id=id)
            thumb.start()
            thumb.join()
            self.set_image(target, id)
            
    def set_image(self, target:Label, id):
        master=target.master
        try: 
            img = PhotoImage(file=f"thumbs/thumb{id}.jpg")
        except:
            img = ImageTk.PhotoImage(Image.open(f"thumbs/thumb{id}.jpg"))
        self.thumbs[str(id)] = img
        target.configure(image=self.thumbs[str(id)], relief="sunken")
        master.update_idletasks()
        target.update()
        
    def download(self, video_id:str, button:Button, audio_only:bool|None=False):
        if audio_only:
            filetype: str = "Audio"
        else:
            filetype: str = "Video"
            
        parent_conn, child_conn = Pipe()
        print(f"download {filetype}...")
        
        if "https://www.youtube.com/watch?v=" in video_id:
            video_link = video_id
        else:
            video_link: str = f"https://www.youtube.com/watch?v={video_id}"
            
        button_id: Button = self.widgets[f"button{button}"]
        button_id.config(text="Verificando...", bg="orange", state="disabled")
        try:
            target = threading.Thread(
                target=youtuber.GetNewVideo, args=(video_link, audio_only, child_conn))
            
            target.start()
            filesize = parent_conn.recv()

            if filesize != None:
                print(str(filesize))
                button_id.config(text=f"Downloading {filetype}: {str(filesize)}kb", bg="green", state="disabled")
                self.myFrame02.update_idletasks()
                target.join()
           
            if parent_conn.recv():
                print("targetJoined")
                button_id.config(text=f"{filetype} Concluido", bg="green", state="normal")
                self.myFrame02.update_idletasks()
                print(f"O download do {filetype} foi concluido.")
            else:
                raise TimeoutError
            
        except:
            button_id.config(text="Erro. Tente Novamente", bg="red", state="normal")
            self.myFrame02.update_idletasks()
            erro = sys.exc_info()
            print(f"Video Indisponivel: {erro}")
        