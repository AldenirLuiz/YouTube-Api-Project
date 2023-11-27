import os
from random import choice
from MyYouTube_API import MyYoutube
from tkinter import Tk,  Frame, Label, Entry, Canvas, Button, Scrollbar, VERTICAL, PhotoImage
import sys 
from PIL import ImageTk, Image
import threading
import youtuber
from multiprocessing import Pipe
from GetThumbs import GetThumb
from manage import MyKeys as Key

FONTS = [
        ("consolas", 22),
        ("arial", 18)]

class MyView:
    def __init__(self, root:Frame) -> None:
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
        self.canvas.bind_all("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")) )
        
    def mouse_event(self, event):
        self.canvas.yview_scroll(int(-1*event.delta/120), "units")

class MyViewController(MyView):
    def __init__(self, root) -> None:
        super().__init__(root)

    def build_view(self, values:list):
        viewFrame = Frame(self.internal_frame)
        for count, item in enumerate(values):
            tempFrame = Frame(viewFrame, relief="ridge", bd=2)
            video_id=item["snippet"]["resourceId"]["videoId"]
            
            # Configurando as propriedades da visualizacao dos dados
            self.widgets.update({
                f"image{count}": Label(tempFrame, text=f"image{count}", image=self.not_found, anchor="sw"),
                f"text{count}": Label( tempFrame, text=f'{item["snippet"]["title"]}', anchor="sw"),
                f"descT{count}": Label(tempFrame, text=f'Canal: {item["snippet"]["channelTitle"]}', anchor="sw"),
                f"descD{count}": Label(tempFrame, text=f'Data: {item["snippet"]["publishedAt"]}', anchor="sw"),
                f"descId{count}": Label(tempFrame, text=f'vId: {item["snippet"]["resourceId"]["videoId"]}', anchor="sw"),
                f"button{count}": Button( # Configurando o botao e a configuracao de funcionalidade
                    tempFrame, text="Download Video", relief="flat", bg="cyan", anchor="center",
                    command=lambda id=video_id, btt=count: 
                    threading.Thread(target=self.download, args=(id, btt)).start()),
                f"button_audio{count}": Button( # Configurando o botao e a configuracao de funcionalidade
                    tempFrame, text="Download Audio", relief="flat", bg="yellow", anchor="center",
                    command=lambda id=video_id, btt=f"_audio{count}": 
                    threading.Thread(target=self.download, args=(id, btt, True)).start())})
            
            # Configurando a posicao do frame de widgets na visualizacao
            tempFrame.pack(expand=1, fill="x",
                ipadx=4, ipady=4, padx=2, pady=2, anchor="center")
            
            try: # Lancando uma requisicao em segundo plano para obter a thumbnail do video 
                target = self.widgets[f"image{count}"]
                url = item["snippet"]["thumbnails"]["default"]["url"]
                _id = item["snippet"]["resourceId"]["videoId"]
                thread = threading.Thread(target=self.get_thumb, args=(target, url, _id))
                thread.start()
            except KeyError:
                # Caso o video estiver indisponivel ou deletado, a thumb nao sera baixada.
                continue
        # Adicionando a visualizacao ao frame principal
        viewFrame.pack(expand=True, fill="both",
            ipadx=4, ipady=4, padx=2, pady=2, anchor="center")
        
        

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
        

class View:
    api_key = choice(Key().keychain)

    def __init__(self) -> None:
        self.window = Tk()
        
        self.mainFrame = Frame(self.window)
        self.mainFrame.pack(expand=True, fill="both")
        
        self.primaryLabel = Label(self.mainFrame, text="Youtube Downloader - By Aldenir", font=FONTS[0])
        self.primaryLabel.pack(expand=0, fill="x", padx=8)
        
        self.divLink = Frame(self.mainFrame, height=40)
        self.divLink.pack(expand=0, fill="both")
        
        self.entryLabel = Label(self.divLink, text="Playlist Link:", font=FONTS[1], anchor='nw')
        self.entryLabel.pack(side="top", expand=False, fill="x")
        self.entry = Entry(self.divLink, width=80)
        self.entry.pack(side="left", expand=1, fill="x", pady=8, padx=0, ipadx=8, ipady=12)
        self.entry.insert(0, "PLmbM7GweQj2sb68py1IDcXicsfJyyBAUt")
        
        self.bttSearch = Button(self.divLink, text="Search", font=FONTS[1], command=lambda:self.load_data())
        self.bttSearch.pack(side="left", expand=0, fill=None)
        
        self.divStatus = Frame(self.mainFrame, relief="solid", bd=2)
        self.divStatus.pack(expand=True, fill="both")
        
        self.statusLabel = Label(self.divStatus, text="Status:", font=FONTS[1], anchor='nw')
        self.statusLabel.pack(side="top", expand=False, fill="x")
        
        self.myView = MyViewController(self.divStatus)
        
    def get_api(self, link:str): # Captura os dados na api do YouTube
        api = MyYoutube(self.api_key, link)
        return api.showVideoInfo()["items"]

    def build(self): # Chama a visualizacao dos dados
        # Pegando os dados da playlist
        #self.primary_frame.destroy() # remove a tela de carregamento
        self.myView.internal_frame.update_idletasks()

        # Para que o scrow da tela possa funcionar precisa configurar o scrollregion
        self.myView.canvas.config(scrollregion=self.myView.canvas.bbox("all"))
        self.window.mainloop() # Passando o loop para o Tkinter
        
    def load_data(self):
        link = self.entry.get()
        if link != str():
            try:
                values=self.get_api(link)
                self.statusLabel.config(text="Status: Link Ok", background="green")
                self.myView.build_view(values)
            except:
                self.statusLabel.config(text="Insira um link Valido!", background="red")
        else:
            self.statusLabel.config(text="Insira um link Valido!", background="red")
        self.myView.show_view()

if __name__ == "__main__":
    # "PLmbM7GweQj2sb68py1IDcXicsfJyyBAUt"
    # "PLt7PgJ6tMUQRDa4C8Jc5_w2AovXNi162G"
    # "PLlBnICoI-g-d-J57QIz6Tx5xtUDGQdBFB"
    # "PLzxQzUX2Qm0lZQbM0SizzgYk0BjaTAy-V"
    # "PLRXpT153SXav_D1T-6U02CSHvXgeL1F69"
    view = View()
    view.build()
    #print(f"Data: {view.get_api()}")
