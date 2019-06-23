from pywinauto import Desktop
from pywinauto.timings import Timings


def action_center(action, enable=False):
    Timings.fast()

    desktop = Desktop(backend='uia')

    action_btn = desktop.taskbar.child_window(class_name='TrayNotifyWnd').action_center
    action_pane = desktop.action_center.child_window(class_name='ScrollViewer')

    if not action_pane.exists():
        action_btn.click()

    for button in action_pane.children():
        if button.element_info.name == action and button.get_toggle_state() != int(enable):
            button.click()
            break

    action_btn.click()


if __name__ == '__main__':
    action_center('Night light', enable=False)
