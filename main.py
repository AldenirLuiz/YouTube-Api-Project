from time import sleep
from googleapiclient.discovery import build
from requests import request
from tkinter import Frame, Label, Tk, Canvas, Button, Scrollbar, VERTICAL
import sys 
import urllib
from PIL import ImageTk
import threading
import youtuber


class MyYoutube:
    def __init__(self, userApi_Key:str, vId:str) -> None:

        self.user_key:str = userApi_Key 
        self.youtube:build = build("youtube", "v3", developerKey=self.user_key, )
        self.id:str = vId
        self.container_videos = list()

    def showVideoInfo(self):
        try:
            my_request = self.youtube.playlistItems().list(
                part="snippet", playlistId=self.id, maxResults=100
            ).execute()
            return my_request
        except:
            self.youtube.search().list(
                q=self.id, part="id, snippet", playlistId=self.id, maxResults=100
            ).execute()
        return 

class MyView:
    def __init__(self, root) -> None:
        
        self.myFrame02:Frame = Frame(root)
        self.widgets = dict()
        self.img_url = dict()
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

        self.myLabel = Label(
            self.internal_frame, text="Videos da Playlist:", 
            font=("consolas", 22)
            ).pack(
            expand=True, fill="both",
            ipadx=4, ipady=4, padx=2, pady=2)
        
        self.myFrame02.pack(
            expand=True, fill="both",
            ipadx=4, ipady=4, padx=2, pady=2)
        
        self.myFrame02.update_idletasks()
        self.internal_frame.update_idletasks()

        self.widgets.update(
            {"master": self.myFrame02}
        )

        # self.canvas.bind_all("<MouseWheelUp>", self.mouse_up)
        self.canvas.bind_all("<MouseWheel>", self.mouse_event)

    def mouse_event(self, event):
        print(event)
        self.canvas.yview_scroll(int(-1*event.delta/120), "units")
        
    def get_thumbs(self, values:list):
        for count, link in enumerate(values):
            temp = GetThumb(link["snippet"]["thumbnails"]["default"]["url"], count)
            temp.start()
            temp.join()
            self.img_url.update({
                f"thumb{count}.jpg": link["snippet"]["thumbnails"]["default"]["url"]})
        
    def build_view(self, values:list):
        #self.get_thumbs(values)
        viewFrame = Frame(self.internal_frame)
        for count, item in enumerate(values):
            tempFrame = Frame(viewFrame, relief="ridge", bd=2)
            try:
                self.img_url.update(
                    {f"thumb{count}.jpg": values[count]["snippet"]["thumbnails"]["default"]["url"]}
                )
                tempFile = GetThumb(self.img_url[f"thumb{count}.jpg"], count)
                tempFile.start()
                # tempFile.join()
                tempImage = f"thumbs/thumb{count}.jpg"
                temp = ImageTk.PhotoImage(file=tempImage)
            except:
                tempImage = "notFound.jpg"
                temp = ImageTk.PhotoImage(file=tempImage)

            
            video_id=item["snippet"]["resourceId"]["videoId"]
            self.widgets.update({
                f"thumb{count}":  temp,
                f"image{count}": Label(tempFrame, text=f"image{count}", image=temp),
                f"text{count}": Label(
                    tempFrame, text=f'{item["snippet"]["title"]}', 
                    font=("consolas", 10), anchor="nw"),
                f"descT{count}": Label(
                    tempFrame, text=f'Canal: {item["snippet"]["channelTitle"]}', 
                    font=("consolas", 10), anchor="nw"),
                f"descD{count}": Label(
                    tempFrame, text=f'Data: {item["snippet"]["publishedAt"]}',
                    font=("consolas", 10), anchor="nw"),
                f"descId{count}": Label(
                    tempFrame, text=f'vId: {item["snippet"]["resourceId"]["videoId"]}', 
                    font=("consolas", 10), anchor="nw"),
                f"button{count}": Button(
                    tempFrame, text="Download", relief="flat", bg="cyan",
                    foreground="orange", activebackground="black", activeforeground="green",
                    command=lambda id=video_id, btt=count: self.download(id, btt)
                )}
            )
            tempFrame.pack(
                expand=True, fill="x",
                ipadx=4, ipady=4, padx=2, pady=2)
        
        viewFrame.pack(
            expand=True, fill="both",
            ipadx=4, ipady=4, padx=2, pady=2)
        self.myFrame02.config(width=600,height=700)
        

    def download(self, video_id, button):
        print("downloading...")
        video_link: str = f"https://www.youtube.com/watch?v={video_id}"
        # print(video_link)
        button_id: Button = self.widgets[f"button{button}"]
        button_id.config(text="Attempt to Download", bg="orange", foreground="white", state="disabled")
        self.myFrame02.update_idletasks()

        try:
            target = youtuber.GetNewVideo(video_link, False, True)
            self.myFrame02.update_idletasks()
            print("O download do video foi concluido.")
            button_id.config(text="Download Concluido", bg="green", foreground="black", state="normal")
            self.myFrame02.update_idletasks()
        except:
            button_id.config(text="Erro. Tente Novamente", bg="red", foreground="black", state="normal")
            self.myFrame02.update_idletasks()
            erro = sys.exc_info()
            print(f"ERRO generico: {erro}")
   
    def show_view(self):
        print("showView")
        index = 0
        for key, widget in self.widgets.items():
            target:Label|Button = widget
            if "image" in key:
                threading.Thread(target=self.set_image, args=(target, key, index)).start()
                # target.configure(image=ImageTk.PhotoImage(file="notFound.jpg"))
                target.pack(side="left", expand=False, fill="x")
                self.myFrame02.update_idletasks()
                
            elif "text" in key:
                target.pack(side="top", expand=False, fill="x")
            elif "desc" in key:
                target.pack(side="top", expand=False, fill="x")
            elif "button" in key:
                target.pack(expand=False, fill="x", anchor="e")
            index+=1
        
        
    def set_image(self, target:Label, key:str, index):

        target.configure(image=GetThumb(self.img_url[f"{key.replace('image', 'thumb')}.jpg"], index))
        target.pack(side="left", expand=False, fill="x")
        self.myFrame02.update_idletasks()
        


class GetThumb(threading.Thread):
        
        def __init__(self, url, id):
            threading.Thread.__init__(self)
            self.url:str = url
            self.id:int = id
            self.fileName:str = str()

        def run(self) -> str:
            try:
                req = request("Get", self.url, timeout=0.800)
                print(f"{self.id}-> {req}")
            except:
                erro = sys.exc_info()
                print(erro[1])
                self.fileName = "notFound.jpg"
                return self.fileName
            
            if req.status_code == 200:
                try:
                    urllib.request.urlretrieve(self.url, f"thumbs/thumb{self.id}.jpg")
                    self.fileName = f"thumbs/thumb{self.id}.jpg"
                    return self.fileName
                except:
                    erro = sys.exc_info()
                    print("Ocorreu um erro:", erro)
                    self.fileName = "notFound.jpg"
                    return self.fileName
            else:
                self.fileName = "notFound.jpg"
                return self.fileName



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
    
