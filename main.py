from argparse import ArgumentParser, ArgumentTypeError
from contextlib import contextmanager
from ctypes import windll

from pyautogui import hotkey, size, moveTo
from pywinauto import Application, Desktop
from pywinauto.application import ProcessNotFoundError

from action_center import action_center


class ControlNotFound(Exception):
    """Raised when the control wasn't found"""


@contextmanager
def block_mouse():
    # Show desktop
    hotkey('win', 'm')

    if bool(windll.shell32.IsUserAnAdmin()):
        windll.user32.BlockInput(True)
        yield
        windll.user32.BlockInput(False)
    else:
        yield

    # Restore minimized windows
    hotkey('shift', 'win', 'm')
    center_mouse()


def check_value(value):
    if 0 <= int(value) <= 100:
        return int(value)
    raise ArgumentTypeError('Value {} not in range [0-100]'.format(value))


def center_mouse():
    x, y = size()
    moveTo(x / 2, y / 2)


def tray_click(button_text: str):
    systray = Desktop(backend='uia').taskbar.child_window(title_re='.*Notification Area')

    for btn in systray.buttons():
        if btn.window_text() == button_text:
            btn.right_click_input()
            break
    else:
        raise ControlNotFound(button_text)


def tray_menuclick(auto_id: str):
    tray_click('OnScreen Control')

    menu = Desktop(backend='uia').dialog.menu

    for item in menu.items():
        if item.automation_id() == auto_id:
            item.click_input()
            break
    else:
        raise ControlNotFound(auto_id)


def start_app():
    cmd = 'C:\\Program Files (x86)\\LG Electronics\\OnScreen Control\\bin\\OnScreen Control.exe'

    try:
        app = Application(backend='uia').connect(path=cmd, timeout=1)
        tray_menuclick('menuStartOSC2')
        window = app.dialog
    except ProcessNotFoundError:
        app = Application(backend='uia').start(cmd, timeout=15)
        window = app.dialog
        window.exists(timeout=15, retry_interval=1)

    window.set_focus()

    return app, window


def start(value):
    _, window = start_app()

    settings_button = window.child_window(auto_id='Btn_MultiMon_MonitorSetting')
    brightness = window.child_window(auto_id='Slider_Brightness')
    contrast = window.child_window(auto_id='Slider_Contrast')

    if settings_button.get_toggle_state() == 0:
        settings_button.click_input()

    brightness.set_value(value)
    contrast.set_value(value)

    window.close()
    tray_menuclick('menuExit')
    # app.kill()

    if value <= 35:
        action_center('Night light', enable=True)
    else:
        action_center('Night light', enable=False)


if __name__ == '__main__':
    parser = ArgumentParser(description='OnScreen Control Brightness Changer')
    parser.add_argument('value', type=check_value, metavar='[0-100]')
    arg = parser.parse_args()

    with block_mouse():
        start(arg.value)
