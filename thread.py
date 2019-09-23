from threading import Thread

import wx

from app.definitions import ID
from automation import auto


class AutomationThread(Thread):

    def __init__(self, window, value):
        Thread.__init__(self)

        self.aborted = False
        self.window = window
        self.value = value

        self.start()

    def run(self):
        auto.start(self.value)
        wx.PostEvent(self.window, ID.CompleteEvent())

    def abort(self):
        self.aborted = True
