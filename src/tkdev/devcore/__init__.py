import tkinter as tk
from tkdev.devicon import Icon_Empty, Icon_TkinterDev


def EmptyFunc():
    pass


class DevAction(object):
    def __init__(self, text: str = "", icon: str = None, command=EmptyFunc):
        self._text = text
        self._icon = icon
        self._command = command

    def wm_icon(self, icon: tk.PhotoImage = None):
        if icon is None:
            pass
        else:
            self._icon = icon
        return self._icon

    icon = wm_icon

    def wm_text(self, text: str = None):
        if text is None:
            pass
        else:
            self._text = text
        return self._text

    text = wm_text

    def wm_command(self, command=None):
        if command is None:
            pass
        else:
            self._command = command
        return self._command

    command = wm_command


class DevSysTray(object):
    def __init__(self, name: str = "", title: str = "", icon: str = Icon_TkinterDev):
        from PIL import Image
        self.menu = []
        self.name = name
        self.title = title
        self.icon = Image.open(icon)

    def add_menu(self, title: str = "", command=EmptyFunc):
        from pystray import MenuItem
        self.menu.append(MenuItem(text=title, action=command))

    def add_action(self, action: DevAction):
        self.add_menu(title=action.text(), command=action.command())

    def show(self):
        from pystray import Icon
        self.Icon = Icon(name=self.name, title=self.title, menu=self.menu, icon=self.icon)
        self.Icon.run()

    def stop(self):
        self.Icon.stop()

    def notify(self, message: str = "", title: str = ""):
        self.Icon.notify()
