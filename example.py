from tkinter import *
from main import MyYoutube, MyView
from PIL import ImageTk, Image


class MyList(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.root = master
        self.pack()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_propagate(False)

        self.canvas = Canvas(self)
        self.canvas.grid(row=0, column=0, sticky="news")

        self.scroll_bar = Scrollbar(self, orient=VERTICAL, command = self.canvas.yview)
        self.scroll_bar.grid(row=0, column=1, sticky='ns')
        self.canvas.config(yscrollcommand = self.scroll_bar.set)
        
        self.internal_frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.internal_frame, anchor='nw')

        self.__build()
        self.internal_frame.update_idletasks()

        self.config(width=800,height=600)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def __build(self):
        api = MyYoutube("PLmbM7GweQj2sb68py1IDcXicsfJyyBAUt")
        itens = api.showVideoInfo()["items"]
        myView = MyView(self.internal_frame)
        myView.build_view(values=itens)

        #myView.show_view()

        for key, widget in myView.images.items():
            target:Label|Button = widget
            if "image" in key:
                target.configure(
                    image=myView.images[f"{str(key).replace('image', 'thumb')}"])
                target.pack(side="left", expand=False, fill="x")
            elif "text" in key:
                target.pack(side="top", expand=False, fill="x")
            elif "desc" in key:
                target.pack(side="bottom", expand=False, fill="x")
            elif "button" in key:
                target.pack(side="right", expand=False, fill="x")
        
if __name__ == "__main__":
    window = Tk()
    my_list = MyList(window)
    window.mainloop()