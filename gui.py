from Tkinter import *
import urllib2
from time import sleep

import thread

from multiprocessing import Lock, Queue

import math


class Application(Frame):

    FRAMERATE = 20
    c = None

    RATIO_MIN = 0.2
    RATIO_MAX = 5.0

    queue = Queue(FRAMERATE)

    req = urllib2.Request(url="http://localhost:8080")

    def update(self):
        ratio = min(self.RATIO_MAX,max(self.RATIO_MIN,float(urllib2.urlopen(self.req).read())))
        print(ratio)
        self.queue.put_nowait(ratio)
        # self.update_graphics(ratio)

    # This method is run only by the main thread
    def process_input_queue(self):
        if not self.queue.empty():
            ratio = self.queue.get_nowait()
            size = int(50*ratio)
            self.c.delete("all")
            self.c.create_rectangle(0, 0, size, size, fill="blue")
            root.update()

    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.pack()
        self.c = Canvas(root)
        self.c.pack()

        while True:
            thread.start_new_thread(self.update,())
            sleep(1.0 / self.FRAMERATE)
            self.process_input_queue()
        self.update()

root = Tk()
root.minsize(width=500, height=500)
app = Application(master=root)
app.mainloop()
root.destroy()