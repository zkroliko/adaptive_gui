from Tkinter import *
import urllib2
from time import sleep

import thread

from multiprocessing import Lock, Queue

import math


class Application(Frame):
    FRAME_RATE = 20
    BASE_SIZE = 50

    RATIO_MIN = 0.2
    RATIO_MAX = 5.0

    req = urllib2.Request(url="http://localhost:8080")

    def update(self):
        ratio = min(self.RATIO_MAX, max(self.RATIO_MIN, float(urllib2.urlopen(self.req).read())))
        print(ratio)
        self.queue.put_nowait(ratio)

    # This method is run only by the main thread
    def process_input_queue(self):
        if not self.queue.empty():
            ratio = self.queue.get_nowait()
            size = int(self.BASE_SIZE * ratio)
            self.c.delete("all")
            self.c.create_rectangle(0, 0, size, size, fill="blue")
            root.update()

    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.pack()
        self.queue = Queue(self.FRAME_RATE)
        self.c = Canvas(root)
        self.c.pack()

        while True:
            thread.start_new_thread(self.update, ())
            sleep(1.0 / self.FRAME_RATE)
            self.process_input_queue()
        self.update()


root = Tk()
root.minsize(width=500, height=500)
app = Application(master=root)
app.mainloop()
root.destroy()
