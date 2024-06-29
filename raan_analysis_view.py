from tkinter import  *
from tkinter import ttk

class RaanAnalysisView:

    def __init__(self, parent) -> None:
        # self.style = ttk.Style()
        self.content = ttk.Frame(parent)
        self.content.pack()

        label = Label(self.content, text="Hello World!")
        label.pack( side = LEFT)
