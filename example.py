from tkinter import Tk, Frame, Label, Button
from PIL import ImageTk, Image
from MyYouTube_API import MyYoutube
from GetThumbs import GetThumb
from threading import Thread

class MainWindow:
    def __init__(self) -> None:
        self.window = Tk()
        self.frame = Frame(self.window)
        self.myImages = dict()
        self.your_api_key = "AIzaSyBjIt3ll9eYs5KZd6Pd1YDfBmfEf6qd6xE"
        self.api = MyYoutube(self.your_api_key, "PLmbM7GweQj2sb68py1IDcXicsfJyyBAUt")
        self.itens = self.api.showVideoInfo()["items"]
        self.not_found = ImageTk.PhotoImage(Image.open("notFound.jpg"))
        self.frame.pack()

    def view(self):
        for index, video in enumerate(self.itens):
            tag = video["snippet"]["title"]
            temp_card = CardView(self.frame, video["snippet"], index=index)
            try:
                url = video["snippet"]["thumbnails"]["default"]["url"]
                thread = Thread(target=self.get_thumb, args=(temp_card.thumb, url, index))
                thread.start()
            except KeyError:
                continue
        self.window.mainloop()
    
    def get_thumb(self, target:Label, url:str, id):
        master=target.master
        thumb = GetThumb(url, id=id)
        thumb.start()
        thumb.join()
        img = ImageTk.PhotoImage(Image.open(thumb.fileName))
        self.myImages[str(id)] = img
        target.configure(image=self.myImages[str(id)], background="red", relief="sunken", bd=4)
        master.update_idletasks()
        target.update()


class CardView:
    def __init__(self, root:Frame, data: dict, index) -> None:
        self.not_found = ImageTk.PhotoImage(Image.open("notFound.jpg"))
        self.frame = Frame(root)
        self.thumb = Label(self.frame, text="", image=self.not_found)
        self.thumb.pack(side="left")
        self.text = Label(self.frame, text=data["title"])
        self.text.pack(side="left")
        self.video_id = data["resourceId"]["videoId"]

        chanel = Label(
            root, text=data["title"], 
            font=("consolas", 10), anchor="nw")
        chanel.pack()

        data_desc = Label(
            root, text=f"Data: {data['publishedAt']}",
            font=("consolas", 10), anchor="nw")
        data_desc.pack()

        vid = Label(
            root, 
            text=f'vId: {self.video_id}', 
            font=("consolas", 10), anchor="nw")
        vid.pack

        btt = Button(
            root, text="Download", relief="flat", bg="cyan",
            foreground="orange", activebackground="black", activeforeground="green",
            command=lambda id=self.video_id, btt=index: Thread(target=self.download, args=(id, btt)).start())
        btt.pack()
        
        self.frame.pack(expand=True, fill="both",ipadx=4, ipady=4, padx=2, pady=2)

    def download(self, id, btt:Button):
        print(f"downloading: {id}")
        btt.configure(text="Baixando...", bg="orange", state="disabled")


        





if __name__ == "__main__":
    main = MainWindow()
    main.view()
