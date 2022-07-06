from tkdev import DevAppBar, DevDrag, DevPopupWindow, DevStatusBar, DevSubWindow, DevToplevel
from tkinter import *
from tkinter import ttk, messagebox

from ctypes import windll
windll.user32.SetProcessDPIAware()


name = "tkdev"
version = "1.5.0"


class DevAppBar_Demo(DevToplevel):
    def __init__(self):
        super(DevAppBar_Demo, self).__init__()
        self.appbar = DevAppBar(self, title="Hello World")
        self.appbar.show()
        self.mainloop()

class DevDrag_Demo(DevToplevel):
    def __init__(self):
        super(DevDrag_Demo, self).__init__()
        self.title("DevDrag测试")
        self.geometry("800x600")

        self.drag_widget = Label(self, text="请拖动我", background="#000000", foreground="#ffffff")
        self.drag_widget.pack(padx=15, pady=15)
        DevDrag(self.drag_widget, self.drag_widget)


class DevMenuBar_Demo(DevToplevel):
    def __init__(self):
        super(DevMenuBar_Demo, self).__init__()
        self.title("DevMenuBar测试")
        self.geometry("400x300")

        self.tip = ttk.Button(self, text="Tip", command=lambda:messagebox.showwarning("警告", "请不要使用这个组件！ 因为里面的内容还为完工，里面未开发任何内容"))
        self.tip.pack(fill=BOTH, expand=YES, padx=15, pady=15)


class DevPopupWindow_Demo(DevToplevel):
    def __init__(self):
        super(DevPopupWindow_Demo, self).__init__()
        self.title("DevPopup测试")
        self.geometry("400x300")

        self.button = ttk.Button(self, text="Click Me")
        self.button.pack(fill=BOTH, expand=YES, padx=15, pady=15)
        self.popup = DevPopupWindow(self, self.button)


class DevStatusBar_Demo(DevToplevel):
    def __init__(self):
        super(DevStatusBar_Demo, self).__init__()
        self.title("DevPopup测试")
        self.geometry("400x300")

        self.statusbar = DevStatusBar(self, "状态栏 | ")
        self.statusbar.show()
        self.statusbar.add_status(self.statusbar, "状态栏 | 状态")
        self.statusbar.add_status(self, "状态栏 | 窗口")


class DevSubWindow_Demo(DevToplevel):
    def __init__(self):
        super(DevSubWindow_Demo, self).__init__()
        self.title("DevPopup测试")
        self.geometry("1080x730")

        self.subwindow = DevSubWindow(self, title="DevSubWindow")
        self.subwindow.show()

class DevToplevel(DevToplevel):
    def __init__(self):
        self.mainloop()