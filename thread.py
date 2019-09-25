from threading import Thread

import wx

from app.definitions import ID
from automation import auto


class AutomationThread(Thread):

    def __init__(self, window, value, button_id):
        Thread.__init__(self)
        self.button_id = button_id
        self.aborted = False
        self.window = window
        self.value = value

        self.start()

    def run(self):
        auto.start(self.value)
        wx.PostEvent(
            self.window,
            ID.CompleteEvent(value=self.value, close_app=self.button_id == ID.SET_CLOSE)
        )

    def abort(self):
        self.aborted = True
