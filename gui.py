import thread
import urllib2
from Tkinter import *
from multiprocessing import Queue
from time import sleep


class Application(Frame):
    FRAME_RATE = 20
    BASE_SIZE = 50

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
            size = int(self.BASE_SIZE * smooth_ratio)
            self.c.delete("all")
            sx, sy, = self.CANVAS_MIDDLE - size, self.CANVAS_MIDDLE - size
            ex, ey = self.CANVAS_MIDDLE + size, self.CANVAS_MIDDLE + size
            self.c.create_rectangle(sx, sy, ex, ey, fill="blue")
            root.update()

    def calculate_ratio(self, new_ratio):
        ratio = (self.old_ratio * self.RATIO_RETENTION + new_ratio) / 2.0
        self.old_ratio = ratio
        return ratio

    def __init__(self, master=None):
        Frame.__init__(self, master)

        # For "moving average"
        self.old_ratio = self.RATIO_DEFAULT

        self.pack()
        self.queue = Queue(self.FRAME_RATE)
        self.c = Canvas(root, width=600, height=600)
        self.c.pack()

        while True:
            thread.start_new_thread(self.retrieve_state, ())
            sleep(1.0 / self.FRAME_RATE)
            self.process_input_queue()
        self.retrieve_state()


root = Tk()
root.minsize(width=500, height=500)
app = Application(master=root)
app.mainloop()
root.destroy()
