from MyYouTube_API import MyYoutube
from requests import request
from tkinter import Tk,  Frame, Label, Canvas, Button, Scrollbar, VERTICAL
import sys 
from PIL import ImageTk, Image
import threading
import youtuber
from multiprocessing import Process, Pipe
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
        self.canvas = Canvas(self.myFrame02, )
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

    def mouse_event(self, event):
        self.canvas.yview_scroll(int(-1*event.delta/120), "units")


    def build_view(self, values:list):
        viewFrame = Frame(self.internal_frame)
        for count, item in enumerate(values):
            tempFrame = Frame(viewFrame, relief="ridge", bd=2)
            video_id=item["snippet"]["resourceId"]["videoId"]

            self.widgets.update({
                f"image{count}": Label(tempFrame, text=f"image{count}", image=self.not_found),
                f"text{count}": Label( tempFrame, text=f'{item["snippet"]["title"]}'),
                f"descT{count}": Label(tempFrame, text=f'Canal: {item["snippet"]["channelTitle"]}'),
                f"descD{count}": Label(tempFrame, text=f'Data: {item["snippet"]["publishedAt"]}'),
                f"descId{count}": Label(tempFrame, text=f'vId: {item["snippet"]["resourceId"]["videoId"]}'),
                f"button{count}": Button(tempFrame, text="Download", relief="flat", bg="cyan",
                    command=lambda id=video_id, btt=count: threading.Thread(target=self.download, args=(id, btt)).start())}
            )
            tempFrame.pack(expand=True, fill="x",
                ipadx=4, ipady=4, padx=2, pady=2)
            
            try:
                target = self.widgets[f"image{count}"]
                url = item["snippet"]["thumbnails"]["default"]["url"]
                thread = threading.Thread(target=self.get_thumb, args=(target, url, count))
                thread.start()
            except KeyError:
                continue
            
            
        viewFrame.pack(expand=True, fill="both",
            ipadx=4, ipady=4, padx=2, pady=2)
        self.myFrame02.config(width=600,height=700)

    def show_view(self):
        for key, widget in self.widgets.items():
            target:Label|Button = widget
            if "image" in key:
                target.pack(side="left", expand=False, fill="x")
                self.internal_frame.update_idletasks()
            elif "text" in key:
                target.pack(side="top", expand=False, fill="x")
            elif "desc" in key:
                target.pack(side="top", expand=False, fill="x")
            elif "button" in key:
                target.pack(expand=False, fill="x", anchor="e")

    def get_thumb(self, target:Label, url:str, id):
        master=target.master
        thumb = GetThumb(url, id=id)
        thumb.start()
        thumb.join()
        img = ImageTk.PhotoImage(Image.open(thumb.fileName))
        self.thumbs[str(id)] = img
        target.configure(image=self.thumbs[str(id)], background="red", relief="sunken", bd=4)
        master.update_idletasks()
        target.update()


    def download(self, video_id, button):
        parent_conn, child_conn = Pipe()
        print("downloading...")
        video_link: str = f"https://www.youtube.com/watch?v={video_id}"
        button_id: Button = self.widgets[f"button{button}"]
        button_id.config(
            text="Attempt to Download", 
            bg="orange", 
            foreground="white", 
            state="disabled"
        )
        try:
            target = threading.Thread(
                youtuber.GetNewVideo(video_link, False, True, child_conn)
            )
            target.start()
            print(parent_conn.recv())
            target.join()
            #print("O download do video foi concluido.")
            button_id.config(text="Download Concluido", bg="green", state="normal")
        except:
            button_id.config(text="Erro. Tente Novamente", bg="red", state="normal")
            self.myFrame02.update_idletasks()
            erro = sys.exc_info()
            print(f"ERRO generico: {erro}")


if __name__ == "__main__":
    your_api_key = "AIzaSyBjIt3ll9eYs5KZd6Pd1YDfBmfEf6qd6xE"
    api = MyYoutube(your_api_key, "PLmbM7GweQj2sb68py1IDcXicsfJyyBAUt")
    itens = api.showVideoInfo()["items"]
    # print(itens[0]["snippet"]["resourceId"]["videoId"])
    view = Tk()
    frmLoading = Frame(view)
    labelLoading = Label(
        frmLoading, text="Carregando...", font=("consolas", 22), anchor="center").pack(
            expand=True, fill="both", anchor="center",
            ipadx=4, ipady=4, padx=2, pady=2
            )
    frmLoading.pack(expand=True, fill="both", anchor="center",
            ipadx=4, ipady=4, padx=2, pady=2)
    view.update_idletasks()

    myView = MyView(view)
    myView.build_view(values=itens)
    frmLoading.destroy()
    myView.show_view()
    myView.internal_frame.update_idletasks()
    myView.canvas.config(scrollregion=myView.canvas.bbox("all"))
    view.after(1000, view.mainloop())
    
