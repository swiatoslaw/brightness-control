import wx
from wx.lib import masked

from ids import ID


class HeaderCtrl(wx.StaticText):

    def __init__(self, parent):
        size = wx.DefaultSize
        font = wx.Font(wx.FontInfo(12))
        style = wx.ALIGN_LEFT

        super(HeaderCtrl, self).__init__(parent, size=size, style=style)

        self.SetFont(font)
        self.SetLabel('Set brightness and contrast value below (0 - 100):')


class ValueField(masked.TextCtrl):

    def __init__(self, parent):
        size = wx.Size(250, -1)
        font = wx.Font(wx.FontInfo(16).Bold().FaceName("Consolas"))
        style = wx.TE_CENTER

        super(ValueField, self).__init__(parent, id=ID.FIELD, size=size, style=style)

        self.SetFont(font)
        self.SetCtrlParameters(mask='###', emptyInvalid=True, formatcodes='V',
                               validRegex=r'^([0-9]\s\s|[1-9][0-9]\s|100)$')
        self.ChangeValue('35')

        self.Bind(wx.EVT_TEXT, self.on_edit)

    # noinspection PyUnusedLocal
    def on_edit(self, event):
        self.Refresh()

        button_set = self.FindWindowById(ID.SET)
        button_set_close = self.FindWindowById(ID.SET_CLOSE)

        if not self.IsValid():
            button_set.Disable()
            button_set_close.Disable()
        else:
            button_set.Enable()
            button_set_close.Enable()


class ValueButtons(wx.BoxSizer):

    def __init__(self, parent):
        self.parent = parent

        size = wx.Size(150, 50)
        font = wx.Font(wx.FontInfo(14))
        flags = wx.SizerFlags().Border(wx.LEFT | wx.RIGHT, 5)

        super(ValueButtons, self).__init__(wx.HORIZONTAL)

        button_35 = wx.Button(parent, label='35%', size=size)
        button_65 = wx.Button(parent, label='65%', size=size)
        button_100 = wx.Button(parent, label='100%', size=size)

        for button in [button_35, button_65, button_100]:
            button.SetFont(font)
            button.Bind(wx.EVT_BUTTON, self.on_button)
            self.Add(button, flags)

    def on_button(self, event):
        value = event.GetEventObject().GetLabel()[:-1]
        self.parent.FindWindowById(ID.FIELD).SetValue(value)


class BottomButtons(wx.BoxSizer):

    def __init__(self, parent):
        font = wx.Font(wx.FontInfo(10))
        flags = wx.SizerFlags().Border(wx.LEFT | wx.RIGHT, 5)

        super(BottomButtons, self).__init__(wx.HORIZONTAL)

        button_set = wx.Button(parent, id=ID.SET, label='Set')
        button_set_close = wx.Button(parent, id=ID.SET_CLOSE, label='Set and Close')
        button_close = wx.Button(parent, id=ID.CLOSE, label='Close')

        for button in [button_set, button_set_close, button_close]:
            button.SetFont(font)
            button.Bind(wx.EVT_BUTTON, self.on_button)
            self.Add(button, flags)

    # noinspection PyMethodMayBeStatic
    def on_button(self, event):
        button_id = event.GetId()

        if button_id == ID.SET:
            # TODO
            print('Clicked on Set!')
        elif button_id == ID.SET_CLOSE:
            # TODO
            print('Clicked on Set and Close!')
        elif button_id == ID.CLOSE:
            event.GetEventObject().GetTopLevelParent().Close(True)


class MainFrame(wx.Frame):

    def __init__(self):
        size = wx.Size(550, 300)  # (width, height)

        super(MainFrame, self).__init__(None, title='Brightness Control', size=size)

        panel = wx.Panel(self, size=size)

        sizer = wx.BoxSizer(orient=wx.VERTICAL)
        sizer.AddMany([
            (HeaderCtrl(panel),    wx.SizerFlags().Border(wx.LEFT | wx.TOP, 20)),
            (ValueField(panel),    wx.SizerFlags().Border(wx.TOP, 15).Center()),
            (ValueButtons(panel),  wx.SizerFlags().Border(wx.TOP, 15).Center()),
            (0, 0, 1),  # AddStretchSpacer(1)
            (BottomButtons(panel), wx.SizerFlags().Border(wx.BOTTOM, 20).Center())
        ])

        panel.SetSizer(sizer)

        self.Show()
        self.Center()


if __name__ == '__main__':
    app = wx.App()
    MainFrame()
    app.MainLoop()
