try:
    from tkinter import *
except ImportError:
    from Tkinter import *


class NewRoot(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.attributes('-alpha', 0.0)

class MyMain(Toplevel):
    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.overrideredirect(1)
        self.attributes('-topmost', 1)
        self.geometry('+100+100')
        self.bind('<ButtonRelease-3>', self.on_close)  #right-click to get out

    def on_close(self, event):
        self.master.destroy()


if __name__ == '__main__':

    root = NewRoot()
    root.lower()
    root.iconify()
    root.title('Spam 2.0')

    app = MyMain(root)
    app.mainloop()