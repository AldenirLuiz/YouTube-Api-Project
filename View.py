
from tkinter import  Frame, Canvas, Scrollbar, VERTICAL
from PIL import ImageTk


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

