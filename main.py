import os
from MyYouTube_API import MyYoutube
from tkinter import Tk,  Frame, Label, Canvas, Button, Scrollbar, VERTICAL
import sys 
from PIL import ImageTk, Image
import threading
import youtuber
from multiprocessing import Pipe
from GetThumbs import GetThumb



class MyView:
    def __init__(self, root:Tk) -> None:
        self.root:Tk = root
        self.myFrame02:Frame = Frame(self.root)
        self.widgets = dict()
        self.thumbs = dict()
        self.myFrame02.grid_rowconfigure(0, weight=1)
        self.myFrame02.grid_columnconfigure(0, weight=1)
        self.myFrame02.grid_propagate(False)
        self.canvas = Canvas(self.myFrame02)
        self.canvas.grid(row=0, column=0, sticky="news")
        self.scroll_bar = Scrollbar(self.myFrame02, orient=VERTICAL, command = self.canvas.yview)
        self.scroll_bar.grid(row=0, column=1, sticky='ns')
        self.canvas.config(yscrollcommand = self.scroll_bar.set)
        self.internal_frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.internal_frame, anchor='nw')
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.not_found = ImageTk.PhotoImage(file="notFound.jpg")
        self.myLabel = Label(
            self.internal_frame, text="Videos da Playlist:", 
            font=("consolas", 22)).pack(expand=True, fill="both",
            ipadx=4, ipady=4, padx=2, pady=2)
        self.myFrame02.pack(expand=True, fill="both",
            ipadx=4, ipady=4, padx=2, pady=2)
        self.myFrame02.update_idletasks()
        self.internal_frame.update_idletasks()
        self.widgets.update(
            {"master": self.myFrame02})
        self.canvas.bind_all("<MouseWheel>", self.mouse_event)

class MyViewController(MyView):
    def __init__(self, root: Tk) -> None:
        super().__init__(root)

    def mouse_event(self, event):
        self.canvas.yview_scroll(int(-1*event.delta/120), "units")

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
                    tempFrame, text="Download", relief="flat", bg="cyan", anchor="center",
                    command=lambda id=video_id, btt=count: 
                    threading.Thread(target=self.download, args=(id, btt)).start()
                )})
            # Configurando a posicao do frame de widgets na visualizacao
            tempFrame.pack(expand=True, fill="x",
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
        self.myFrame02.config(width=600,height=700)

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
                target.pack(expand=False, fill="x")

    def get_thumb(self, target:Label, url:str, id):
        master=target.master

        if os.path.exists(f"{os.path.dirname(__file__)}\\thumbs\\thumb{id}.jpg"):
            self.set_image(target, id)
        else:
            thumb = GetThumb(url, id=id)
            thumb.start()
            thumb.join()
            self.set_image(target, id)
            
    def set_image(self, target:Label, id):
        master=target.master
        img = ImageTk.PhotoImage(Image.open(f"thumbs/thumb{id}.jpg"))
        self.thumbs[str(id)] = img
        target.configure(image=self.thumbs[str(id)], background="red", relief="sunken")
        master.update_idletasks()
        target.update()
        


    def download(self, video_id, button):
        parent_conn, child_conn = Pipe()
        print("downloading...")
        video_link: str = f"https://www.youtube.com/watch?v={video_id}"
        button_id: Button = self.widgets[f"button{button}"]
        button_id.config(text="Downloading...", bg="orange", state="disabled")
        try:
            target = threading.Thread(
                youtuber.GetNewVideo(video_link, False, True, child_conn))
            target.start()
            print(parent_conn.recv())
            target.join()
            #print("O download do video foi concluido.")
            button_id.config(text="Concluido", bg="green", state="normal")
        except:
            button_id.config(text="Erro. Tente Novamente", bg="red", state="normal")
            self.myFrame02.update_idletasks()
            erro = sys.exc_info()
            print(f"ERRO generico: {erro}")
        

class View:
    fonts = [
        ("consolas", 22),
        ("arial", 16)]
    api_key = "AIzaSyBjIt3ll9eYs5KZd6Pd1YDfBmfEf6qd6xE"

    def __init__(self, playlist_key:str) -> None:
        self.window = Tk() # Inicializando janela principal
        self.primary_frame = Frame(self.window)
        self.primary_label = Label(self.primary_frame, text="Carregando...")
        self.primary_frame.pack()
        self.primary_label.pack()
        self.primary_frame.update_idletasks()
        # Inicializado o Id da playlist
        self.playlist = playlist_key

        self.myView = MyViewController(self.window)
        
    def get_api(self): # Captura os dados na api do YouTube
        api = MyYoutube(self.api_key, self.playlist)
        return api.showVideoInfo()["items"]

    def build(self): # Chama a visualizacao dos dados
        # Pegando os dados da playlist
        self.myView.build_view(values=self.get_api())
        self.myView.show_view()

        self.primary_frame.destroy() # remove a tela de carregamento
        self.myView.internal_frame.update_idletasks()

        # Para que o scrow da tela possa funcionar precisa configurar o scrollregion
        self.myView.canvas.config(scrollregion=self.myView.canvas.bbox("all"))
        self.window.mainloop() # Passando o loop para o Tkinter

if __name__ == "__main__":
    # "PLmbM7GweQj2sb68py1IDcXicsfJyyBAUt")
    view = View("PLmbM7GweQj2sb68py1IDcXicsfJyyBAUt")
    view.build()
