import wx
import wx.lib.newevent


class ID:
    FIELD = wx.NewIdRef()
    SET = wx.NewIdRef()
    SET_CLOSE = wx.NewIdRef()
    CLOSE = wx.ID_CLOSE

    CompleteEvent, EVT_COMPLETE = wx.lib.newevent.NewEvent()
