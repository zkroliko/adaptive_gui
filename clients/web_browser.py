import urllib2
from multiprocessing import Queue

import thread
from time import sleep

from tkinterhtml import *
from Tkinter import *

class Application(Frame):
    FRAME_RATE = 20

    GENERAL_SCALE = 0.5

    RATIO_MIN = 0.2
    RATIO_DEFAULT = 1.0
    RATIO_MAX = 8.0

    RATIO_RETENTION = 0.9

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
            self.update_frame(smooth_ratio)
            root.update()

    def update_frame(self, ratio):
        self.frame.html.configure(fontscale=round(ratio*self.GENERAL_SCALE,1))

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

        # Html

        self.html = self.retrieve_html("https://en.wikipedia.org/wiki/Computer_vision")

        # Html frame
        self.frame = HtmlFrame(root, horizontal_scrollbar="auto")
        self.frame.set_content(self.html)
        self.frame.html.configure(fontscale=self.RATIO_DEFAULT)
        self.frame.pack()
        root.update()

        while True:
            thread.start_new_thread(self.retrieve_state, ())
            sleep(1.0 / self.FRAME_RATE)
            self.process_input_queue()

    def retrieve_html(self, url):
        content = urllib2.urlopen(url).read()
        without_head = re.sub(r'<head>.*<\/head>',' ',content, flags=re.DOTALL)
        return re.sub(r'<script>.*<\/script>','', without_head, flags=re.DOTALL)

root = Tk()
root.minsize(width=1200, height=600)
app = Application(master=root)
app.mainloop()
root.destroy()