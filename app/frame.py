import wx

from app.definitions import ID
from app.widgets import HeaderCtrl, ValueField, ValueButtons, BottomButtons
from thread import AutomationThread


# noinspection PyUnusedLocal
class MainFrame(wx.Frame):

    def __init__(self):
        super(MainFrame, self).__init__(None, title='Brightness Control', size=wx.Size(550, 300))
        self.setup_ui()

        self.worker = None

        # Setup events
        self.Bind(ID.EVT_COMPLETE, self.on_complete)
        self.FindWindowById(ID.SET).Bind(wx.EVT_BUTTON, self.on_set)
        self.FindWindowById(ID.SET_CLOSE).Bind(wx.EVT_BUTTON, self.on_set)
        self.FindWindowById(ID.CLOSE).Bind(wx.EVT_BUTTON, lambda event: self.Close(True))

    def setup_ui(self):
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(orient=wx.VERTICAL)
        sizer.AddMany([
            (HeaderCtrl(panel), wx.SizerFlags().Border(wx.LEFT | wx.TOP, 20)),
            (ValueField(panel), wx.SizerFlags().Border(wx.TOP, 15).Center()),
            (ValueButtons(panel), wx.SizerFlags().Border(wx.TOP, 15).Center()),
            (0, 0, 1),  # AddStretchSpacer(1)
            (BottomButtons(panel), wx.SizerFlags().Border(wx.BOTTOM, 20).Center())
        ])
        panel.SetSizer(sizer)

        self.Show()
        self.Center()

    def on_set(self, event):
        if not self.worker:
            self.Iconize()
            value = self.FindWindowById(ID.FIELD).GetValue()
            self.worker = AutomationThread(self, value)

    def on_complete(self, event):
        self.Restore()
        self.Raise()
        self.worker = None
