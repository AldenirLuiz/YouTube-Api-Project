import threading
from tkinter import Frame, Label, Button
from View import MyView


class MyVideoView(MyView):
    def __init__(self, root: Frame) -> None:
        super().__init__(root)
        self.mainFrame = Frame(self.internal_frame, relief="ridge", bd=4)
        self.mainFrame.pack(expand=1, fill="both")
        
    def build_view(self, values: list):
        for indexer, video in enumerate(values["formats"]):
            #print(f"{video}")
            tempFrame = Frame(self.mainFrame)
            tempLabelQualit = Label(tempFrame, text=f"Qualit: {video['qualityLabel']}", anchor="nw").pack(expand=1, fill="x")
            tempLabelAudio = Label(tempFrame, text=f"Audio: {video['audioQuality']}", anchor="nw").pack(expand=1, fill="x")
            tempLabelFormat = Label(tempFrame, text=f"Format: {video['mimeType']}", anchor="nw").pack(expand=1, fill="x")
            tempBt = Button( # Configurando o botao e a configuracao de funcionalidade
                tempFrame, text="Download Audio", relief="flat", bg="yellow", anchor="center",
                command=lambda id="", btt=f"_audio{indexer}": 
                threading.Thread(target=self.download, args=(id, btt, True)).start()).pack()
            tempFrame.pack(expand=1, fill="both")