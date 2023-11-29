from multiprocessing import Pipe
from random import choice
from manage import MyKeys as Key
from tkinter import Tk, Frame, Label, Entry, Button
from my_view_controller import MyViewController
from my_view_controller_video import MyVideoView
from MyYouTube_API import MyYoutube
from youtuber import GetNewVideo

FONTS = [("consolas", 22), ("arial", 18)]

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
        self.entry.insert(0, "https://www.youtube.com/watch?v=LXb3EKWsInQ&t=82s")
        
        self.bttSearch = Button(self.divLink, text="Search", font=FONTS[1], command=lambda:self.load_data())
        self.bttSearch.pack(side="left", expand=0, fill=None)
        
        self.divStatus = Frame(self.mainFrame, relief="solid", bd=2)
        self.divStatus.pack(expand=True, fill="both")
        
        self.statusLabel = Label(self.divStatus, text="Status:", font=FONTS[1], anchor='nw')
        self.statusLabel.pack(side="top", expand=False, fill="x")
        
        self.myView = MyViewController(self.divStatus)
        
    def get_api(self, link:str): # Captura os dados na api do YouTube
        
        if "&list=" in link:
            linked = link[link.index("&list=")::].replace("&list=", "") # limpando id da playlist
        elif "https://www.youtube.com/watch?v=" in link:
            return GetNewVideo(link, False).get_viedeo_res
        else:
            linked = link
            
        api = MyYoutube(self.api_key, linked)
        return api.showVideoInfo()["items"]

    def build(self): # Chama a visualizacao dos dados
        # Pegando os dados da playlist
        #self.myViewPlaylist.internal_frame.update_idletasks()

        # Para que o scrow da tela possa funcionar precisa configurar o scrollregion
        #self.myViewPlaylist.canvas.config(scrollregion=self.myViewPlaylist.canvas.bbox("all"))
        self.window.mainloop() # Passando o loop para o Tkinter
        
    def load_data(self):
        link = self.entry.get()
        parent_conn, child_conn = Pipe()
        self.myView.clear_view()
        self.myView = MyViewController(self.divStatus)
        
        
        if link != str():
            
            if "&list=" in link:
                self.statusLabel.config(text="Carregando...", background="yellow")
                values=self.get_api(link)
                self.myView.build_view(values)
                self.divStatus.update_idletasks()
                
            else:
                self.statusLabel.config(text="Carregando...", background="yellow")
                self.divStatus.update_idletasks()
                values = GetNewVideo(link, False, parent_conn).get_viedeo_res()
                self.myView.build_view_video(values)
                
            self.myView.show_view()
            self.myView.configscroll()
            self.statusLabel.config(text="Link OK.", background="green")
            self.divStatus.pack()
        else:
            self.statusLabel.config(text="Insira um link Valido!", background="red")
        self.mainFrame.update_idletasks()
        

if __name__ == "__main__":
    # "PLmbM7GweQj2sb68py1IDcXicsfJyyBAUt"
    # "PLt7PgJ6tMUQRDa4C8Jc5_w2AovXNi162G"
    # "PLlBnICoI-g-d-J57QIz6Tx5xtUDGQdBFB"
    # "PLzxQzUX2Qm0lZQbM0SizzgYk0BjaTAy-V"
    # "PLRXpT153SXav_D1T-6U02CSHvXgeL1F69"
    # "https://www.youtube.com/watch?v=0MiR7bC9B5o&list=PL6NdkXsPL07KN01gH2vucrHCEyyNmVEx4"
    # "https://www.youtube.com/watch?v=MczwQBm6c8E&list=PLxE6Fka6c_h232PqP-We5HQuJdh79RWoJ"
    # video: "https://www.youtube.com/watch?v=MczwQBm6c8E" 720p
    # video: "https://www.youtube.com/watch?v=aciSf8ZRqS8" 1080p
    # video: "https://www.youtube.com/watch?v=LXb3EKWsInQ&t=82s" 4k
    view = View()
    view.build()
    #print(f"Data: {view.get_api()}")