import thread
import urllib2
from Tkinter import *

import numpy as np
from multiprocessing import Queue
from time import sleep


class Application(Frame):
    FRAME_RATE = 20

    CANVAS_SIZE = 600
    CANVAS_MIDDLE = CANVAS_SIZE / 2

    RATIO_MIN = 0.2
    RATIO_DEFAULT = 1.0
    RATIO_MAX = 8.0

    RATIO_RETENTION = 0.4

    req = urllib2.Request(url="http://localhost:8080")

    def retrieve_state(self):
        try:
            retrieved_data = urllib2.urlopen(self.req).read()
            ratio = min(self.RATIO_MAX, max(self.RATIO_MIN, float(retrieved_data)))
            print(ratio)
            self.queue.put_nowait(ratio)
        except urllib2.URLError:
            print("Failed to update")

    # This method is run only by the main thread
    def process_input_queue(self):
        if not self.queue.empty():
            received_ratio = self.queue.get_nowait()
            smooth_ratio = self.calculate_ratio(received_ratio)
            self.update_image(smooth_ratio)
            root.update()

    def update_image(self, ratio):
        nom, denom = int(ratio * 2), 3
        if (nom, denom) != self.old_scaling_factor:
            print("aaa")
            self.old_scaling_factor = nom, denom
            self.c.delete(self.image)
            zoomed = self.photoImg.zoom(nom, nom)
            self.display_image = zoomed.subsample(denom, denom)
            self.image = self.c.create_image(2 * self.CANVAS_MIDDLE, self.CANVAS_MIDDLE, image=self.display_image)

    def calculate_ratio(self, new_ratio):
        ratio = (self.old_ratio * self.RATIO_RETENTION + new_ratio) / 2.0
        self.old_ratio = ratio
        return ratio

    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.pack()

        # For sync
        self.queue = Queue(self.FRAME_RATE)

        # For "moving average"
        self.old_ratio = self.RATIO_DEFAULT

        # Canvas
        self.c = Canvas(root, width=2 * self.CANVAS_SIZE, height=self.CANVAS_SIZE)
        self.c.pack()

        # Image to show in the canvas
        self.photoImg = PhotoImage(file='image.gif')
        self.display_image = self.photoImg
        self.image = self.c.create_image(2 * self.CANVAS_MIDDLE, self.CANVAS_MIDDLE, image=self.photoImg)

        # For performance sake
        self.old_scaling_factor = None

        root.update()

        while True:
            thread.start_new_thread(self.retrieve_state, ())
            self.process_input_queue()
            sleep(1.0 / self.FRAME_RATE)


root = Tk()
root.minsize(width=2 * Application.CANVAS_SIZE, height=Application.CANVAS_SIZE)
app = Application(master=root)
app.mainloop()
root.destroy()
