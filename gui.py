from Tkinter import *
import json
import urllib2
from time import sleep


class Application(Frame):

    FRAMERATE = 10
    c = None

    def update(self):
        ratio = urllib2.urlopen("http://localhost:8080").read(4)
        self.updateRectangle(ratio)

    def updateRectangle(self,ratio):
        h, w = 100, 100
        self.c.create_rectangle(100, 100, (100+h)*ratio, (100+w)*ratio, fill="blue")

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.c = Canvas(root)
        self.c.pack()

        while True:
            sleep(1 / self.FRAMERATE)
            root.update()
            self.update()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()