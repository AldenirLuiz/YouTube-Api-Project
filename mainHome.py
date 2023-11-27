from tkinter import *


class mainHome:
    fonts = [
        ("consolas", 22),
        ("arial", 16)]
    def __init__(self) -> None:
        self.mainWindow = Tk()
        self.mainWindow.geometry("600x300")
        
        self.mainFrame = Frame(self.mainWindow)
        self.mainFrame.pack()
        
        self.primaryLabel = Label(self.mainFrame, text="Youtube Downloader - By Aldenir", font=self.fonts[0])
        self.primaryLabel.pack()
        
        self.divLink = Frame(self.mainFrame, width=100, height=300)
        self.divLink.pack(side="top", expand=True, fill="both", padx=22, pady=22)
        
        self.entryLabel = Label(self.divLink, text="Playlist Link:", font=self.fonts[1], anchor='nw')
        self.entryLabel.pack(side="top", expand=False, fill="both")
        self.entry = Entry(self.divLink, width=50)
        self.entry.pack(side="left", expand=True, fill="both")
        self.bttSearch = Button(self.divLink, text="Search", font=self.fonts[1])
        self.bttSearch.pack(side="left", expand=True, fill="both")
        
        self.divStatus = Frame(self.mainFrame, relief="solid", bd=2, width=200, height=300)
        self.divStatus.pack(side="bottom", expand=True, fill="both", padx=22, pady=8)
        
        self.statusLabel = Label(self.divStatus, text="Status:", font=self.fonts[1], anchor='nw')
        self.statusLabel.pack(side="top", expand=False, fill="both")
        
        
        self.mainWindow.mainloop()


mainHome()