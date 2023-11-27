from tkinter import *
from tkinter import ttk

root = Tk()

# criar container principal
mainFrame = Frame(root)
mainFrame.pack(expand=True, fill="both")

# criar canvas para receber o conteudo rolavel
mainCanvas = Canvas(mainFrame)
mainCanvas.pack(side="left", expand=True, fill="both")

# criar o scrolbar
myScrollbar = ttk.Scrollbar(mainFrame, orient="vertical", command=mainCanvas.yview)
myScrollbar.pack(side="right", expand=True, fill="y")

# configurar o canvas
mainCanvas.configure(yscrollcommand=myScrollbar.set)
mainCanvas.bind("<Configure>", lambda e: mainCanvas.configure(scrollregion=mainCanvas.bbox("all")))

# criar frame secundaria
secFrame = Frame(mainCanvas)

#criar window com frame secundaria
mainCanvas.create_window((0,0), window=secFrame, anchor="nw")


for i in range(100):
    Button(secFrame, text=f"button_{i}").pack()
    

root.mainloop()