from Tkinter import *
import json
import urllib2
from time import sleep


class Application(Frame):

    FRAMERATE = 20
    c = None

    def update(self):
        ratio = float(urllib2.urlopen("http://localhost:8080").read(6))
        print(1.0/ratio)
        self.update_rectangle(1.0 / (ratio + 0.001))
        root.update()

    def update_rectangle(self, ratio):
        size = int(50*ratio)
        self.c.delete("all")
        self.c.create_rectangle(0, 0, size, size, fill="blue")

    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.pack()
        self.c = Canvas(root)
        self.c.pack()

        while True:
            sleep(1.0 / self.FRAMERATE)
            self.update()

root = Tk()
root.minsize(width=500, height=500)
app = Application(master=root)
app.mainloop()
root.destroy()