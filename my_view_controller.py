from tkinter import Frame, Label, Button, PhotoImage, Canvas,Scrollbar, VERTICAL
from GetThumbs import GetThumb
import threading
import youtuber
import os
import sys 
from multiprocessing import Pipe
from PIL import ImageTk, Image
from View import MyView

FONTS = [("consolas", 22), ("arial", 14)]

class MyViewController(MyView):
    def __init__(self, root) -> None:
        self.myFrame02:Frame = Frame(root)
        
        self.widgets = dict()
        self.thumbs = dict()
        
        self.canvas = Canvas(self.myFrame02)
        self.canvas.pack(side="left", expand=True, fill="both")
        
        self.scroll_bar = Scrollbar(self.myFrame02, orient=VERTICAL, command=self.canvas.yview)
        self.scroll_bar.pack(side="right", expand=0, fill="y")
        
        self.canvas.config(yscrollcommand = self.scroll_bar.set)
        
        self.internal_frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.internal_frame, anchor='nw')
        
        self.not_found = ImageTk.PhotoImage(file="notFound.jpg")
        
        self.myFrame02.pack(expand=1, fill="both", ipadx=4, ipady=4, padx=2, pady=2)
        self.myFrame02.update_idletasks()
        
        self.internal_frame.update_idletasks()
        self.widgets.update(
            {"master": self.myFrame02})
        
        self.canvas.bind_all("<MouseWheel>", self.mouse_event)
        self.canvas.bind_all("<Configure>", self.setScrollRegion)
        
    def mouse_event(self, event):
        self.canvas.yview_scroll(int(-1*event.delta/120), "units")
        
    def setScrollRegion(self, event):
        try:
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        except:
            pass
    
    def clear_view(self):
        self.widgets = dict()
        self.myFrame02.destroy()

    def build_view(self, values:list):
        
        for count, item in enumerate(values):
            tempFrame = Frame(self.internal_frame, relief="ridge", bd=2)
            
            self.config_data_playList(item, count, tempFrame)
            self.request_thumb(item, count)
            
            # Configurando a posicao do frame de widgets na visualizacao
            tempFrame.pack(expand=1, fill="x",
                ipadx=4, ipady=4, padx=2, pady=2, anchor="center")
            
        
    def build_view_video(self, values: dict):
        video_id = values["id"]
        thumb = values["thumb"]
        for indexer, video in enumerate(values["data"]["adaptiveFormats"]):
            #print(f"{video}")
            tempFrame = Frame(self.internal_frame, relief="ridge", bd=2)
            self.widgets.update({
            f"image{indexer}": Label(tempFrame, text=f"image{indexer}", image=self.not_found, anchor="sw"),
            f"text{indexer}Qualit":  Label(tempFrame, text=f"Qualit: {video['quality']}", anchor="nw", font=FONTS[0]),
            f"text{indexer}Framerate": Label(tempFrame, text=f"fps: {video.get('fps')}", anchor="nw", font=FONTS[1]),
            f"text{indexer}Format": Label(tempFrame, text=f"Format: {video['mimeType']}", anchor="nw", font=FONTS[1]),
            f"text{indexer}Size": Label(tempFrame, text=f"Size: {round(int(video['contentLength'])/1024)}KB", anchor="nw", font=FONTS[1]),
            
            f"button{indexer}": Button( # Configurando o botao e a configuracao de funcionalidade
                tempFrame, text="Download Video", relief="flat", bg="cyan", anchor="center",
                command=lambda id=video_id, btt=indexer: 
                threading.Thread(target=self.download, args=(id, btt)).start()),
            f"button_audio{indexer}": Button( # Configurando o botao e a configuracao de funcionalidade
                tempFrame, text="Download Audio", relief="flat", bg="yellow", anchor="center",
                command=lambda id=video_id, btt=f"_audio{indexer}": 
                threading.Thread(target=self.download, args=(id, f"button_audio{indexer}", True)).start())})
            self.request_thumb({}, indexer, thumb, f"vid{indexer}-{video_id}")
            tempFrame.pack(expand=1, fill="both", padx=8, pady=8, ipadx=4, ipady=4)
        
    def config_data_playList(self, item, indexer:int, root):
        
        video_id=item["snippet"]["resourceId"]["videoId"]
        # Configurando as propriedades da visualizacao dos dados
        self.widgets.update({
            f"image{indexer}": Label(root, text=f"image{indexer}", image=self.not_found, anchor="sw"),
            f"text{indexer}": Label( root, text=f'{item["snippet"]["title"]}', anchor="sw",font=FONTS[0]),
            f"descT{indexer}": Label(root, text=f'Canal: {item["snippet"]["channelTitle"]}', anchor="sw",font=FONTS[1]),
            f"descD{indexer}": Label(root, text=f'Data: {item["snippet"]["publishedAt"]}', anchor="sw",font=FONTS[1]),
            f"descId{indexer}": Label(root, text=f'vId: {item["snippet"]["resourceId"]["videoId"]}', anchor="sw",font=FONTS[1]),
            f"button{indexer}": Button( # Configurando o botao e a configuracao de funcionalidade
                root, text="Download Video", relief="flat", bg="cyan", anchor="center",
                command=lambda id=video_id, btt=indexer: 
                threading.Thread(target=self.download, args=(id, btt)).start()),
            f"button_audio{indexer}": Button( # Configurando o botao e a configuracao de funcionalidade
                root, text="Download Audio", relief="flat", bg="yellow", anchor="center",
                command=lambda id=video_id, btt=f"_audio{indexer}": 
                threading.Thread(target=self.download, args=(id, btt, True)).start())})
    
    
    def request_thumb(self, item, indexer, url:str=None, id:str=None) -> bool:
        if url:
            _url = url
        else:
            try:
                _url = item["snippet"]["thumbnails"]["default"]["url"]
            except KeyError:
                return False
        if id:
            _id = id
        else:
            _id = item["snippet"]["resourceId"]["videoId"]
        
        try: # Lancando uma requisicao em segundo plano para obter a thumbnail do video 
                target = self.widgets[f"image{indexer}"]
                thread = threading.Thread(target=self.get_thumb, args=(target, _url, _id))
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
            img_temp = Image.open(f"thumbs/thumb{id}.jpg")
            img_res = img_temp.resize((256, 192), 3)
            img = ImageTk.PhotoImage(img_res)
            
        self.thumbs[str(id)] = img
        target.configure(image=self.thumbs[str(id)], relief="sunken", width=256, height=192)
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
            target = threading.Thread(target=youtuber.GetNewVideo(video_link, audio_only, child_conn).get_video())
            
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
        