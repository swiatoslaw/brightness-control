import wx

from app.definitions import ID
from app.widgets import HeaderCtrl, ValueField, ValueButtons, BottomButtons
from thread import AutomationThread


# noinspection PyUnusedLocal
class MainFrame(wx.Frame):

    def __init__(self):
        super(MainFrame, self).__init__(None, title='Brightness Control', size=wx.Size(550, 300))

        self.panel = wx.Panel(self)
        self.field = ValueField(self.panel)
        self.buttons = BottomButtons(self.panel)

        self.setup_ui()

        self.button_set = self.buttons.button_set
        self.button_set_close = self.buttons.button_set_close
        self.button_close = self.buttons.button_close

        self.worker = None

        # Setup events
        self.Bind(ID.EVT_COMPLETE, self.on_complete)
        self.button_set.Bind(wx.EVT_BUTTON, self.on_set)
        self.button_set_close.Bind(wx.EVT_BUTTON, self.on_set)
        self.button_close.Bind(wx.EVT_BUTTON, lambda event: self.Close(True))

    def setup_ui(self):
        sizer = wx.BoxSizer(orient=wx.VERTICAL)
        sizer.AddMany([
            (HeaderCtrl(self.panel), wx.SizerFlags().Border(wx.LEFT | wx.TOP, 20)),
            (self.field, wx.SizerFlags().Border(wx.TOP, 15).Center()),
            (ValueButtons(self.panel), wx.SizerFlags().Border(wx.TOP, 15).Center()),
            (0, 0, 1),  # AddStretchSpacer(1)
            (self.buttons, wx.SizerFlags().Border(wx.BOTTOM, 20).Center())
        ])
        self.panel.SetSizer(sizer)

        self.Show()
        self.Center()

    def on_set(self, event):
        if not self.worker:
            self.Iconize()
            value = self.field.GetValue()
            self.worker = AutomationThread(self, value, event.GetId())

    def on_complete(self, event):
        if event.close_app:
            self.Close(True)

        self.Restore()
        self.Raise()
        self.worker = None
