from argparse import ArgumentParser, ArgumentTypeError
from contextlib import contextmanager
from ctypes import windll

import pyautogui
from pywinauto import Application, Desktop
from pywinauto.application import ProcessNotFoundError


@contextmanager
def block_mouse():
    windll.user32.BlockInput(True)
    yield
    windll.user32.BlockInput(False)


def check_value(value):
    if 0 <= int(value) <= 100:
        return int(value)
    raise ArgumentTypeError('value {} not in range [0-100]'.format(value))


def center_mouse() -> None:
    x, y = pyautogui.size()
    pyautogui.moveTo(x / 2, y / 2)


def systray_rclick(text: str):
    systray = Application().connect(path='explorer').ShellTrayWnd.NotificationAreaToolbar

    for i in range(systray.button_count()):
        if systray.button(i).text() == text:
            systray.button(i).click_input('right')
            break
    else:
        raise RuntimeError('System tray button "{}" not found!'.format(text))


def systray_menu_click(automation_id: str):
    systray_rclick('OnScreen Control')

    menu = Desktop(backend='uia').dialog.menu

    for item in menu.items():
        if item.automation_id() == automation_id:
            item.click_input()
            break
    else:
        raise RuntimeError('Menu option "{}" not found!'.format(automation_id))


def start_app():
    cmd = 'C:\\Program Files (x86)\\LG Electronics\\OnScreen Control\\bin\\OnScreen Control.exe'

    try:
        app = Application(backend='uia').connect(path=cmd, timeout=1)
        systray_menu_click('menuStartOSC2')
        window = app.dialog
        window.set_focus()

    except ProcessNotFoundError:
        app = Application(backend='uia').start(cmd, timeout=15)
        window = app.dialog
        window.exists(timeout=15, retry_interval=1)
        window.set_focus()

    return app, window


def start(value):
    _, window = start_app()

    settings_button = window.child_window(auto_id='Btn_MultiMon_MonitorSetting')
    brightness = window.child_window(auto_id="Slider_Brightness")
    contrast = window.child_window(auto_id="Slider_Contrast")

    if settings_button.get_toggle_state() == 0:
        settings_button.click_input()

    brightness.set_value(value)
    contrast.set_value(value)

    window.close()
    systray_menu_click('menuExit')
    # app.kill()


if __name__ == "__main__":
    parser = ArgumentParser(description='OnScreen Control Brightness Changer')
    parser.add_argument('value', type=check_value, metavar='[0-100]')
    arg = parser.parse_args()

    with block_mouse():
        start(arg.value)

    center_mouse()
