from tkdev import *
from tkdev.devdemo import DevAppBar_Demo, DevDrag_Demo, DevMenuBar_Demo, DevPopupWindow_Demo, DevStatusBar_Demo, DevSubWindow_Demo, DevToplevel_Demo


class devdemo(tk.Tk):
    def __init__(self):
        super(devdemo, self).__init__()
        self.title("tkdev demos")
        self.geometry("760x440")

        self.paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL, height=3)

        self.choices_frame = tk.Frame(self)
        self.choices_yscroll = ttk.Scrollbar(self.choices_frame, orient=tk.VERTICAL)
        self.choices_yscroll.pack(fill=tk.Y, side=tk.RIGHT)
        self.choices_xscroll = ttk.Scrollbar(self.choices_frame, orient=tk.HORIZONTAL)
        self.choices_xscroll.pack(fill=tk.X, side=tk.BOTTOM)
        self.choices = tk.Listbox(self.choices_frame, borderwidth=1, selectborderwidth=0, relief=tk.FLAT, bd=0,
                                  yscrollcommand=self.choices_yscroll.set, xscrollcommand=self.choices_xscroll.set,
                                  justify=tk.LEFT)
        self.choices.pack(fill=tk.BOTH, side=tk.LEFT, expand=1)
        self.choices_yscroll.configure(command=self.choices.yview)
        self.choices_xscroll.configure(command=self.choices.xview)
        for item in ["DevAccumulatorButton", "DevAppBar", "DevDrag", "DevImage",
                     "DevMenu", "DevMenuBar", "DevPopupWindow", "DevStatusBar",
                     "DevSubWindow", "DevToolTip", "DevTitleBar", "DevWindow",
                     "DevToplevel",
                     "All"]:
            self.choices.insert(tk.END, item)
        self.paned.add(self.choices_frame)

        self.preview = ttk.Frame(self)
        self.preview_button = ttk.Button(self.preview, text="预览", command=self.preview_demo)
        self.preview_button.pack(fill=tk.BOTH, expand=tk.YES, padx=15, pady=15)
        self.paned.add(self.preview)

        self.paned.pack(fill=tk.BOTH, expand=tk.YES)

    def preview_demo(self):
        try:
            self.preview_list = self.choices.get(self.choices.curselection())
            print(self.preview_list)
        except tk.TclError:
            pass
        else:
            if self.preview_list == "DevDrag":
                demo = DevDrag_Demo()
                demo.mainloop()
            elif self.preview_list == "DevMenuBar":
                demo = DevMenuBar_Demo()
                demo.mainloop()
            elif self.preview_list == "DevPopupWindow":
                demo = DevPopupWindow_Demo()
                demo.mainloop()
            elif self.preview_list == "DevStatusBar":
                demo = DevStatusBar_Demo()
                demo.mainloop()
            elif self.preview_list == "DevSubWindow":
                demo = DevSubWindow_Demo()
                demo.mainloop()
            elif self.preview_list == "All":
                import tkdev as dev
                import tkinter as tk
                import tkinter.ttk as ttk

                root = dev.DevToplevel()
                root.geometry("300x350")
                statusbar = dev.DevStatusBar(root, default_text="状态栏 | ")
                root.statusbar(statusbar)
                titlebar = dev.DevTitleBar(root, iswindow=True, window=root, title_label="Dev")
                statusbar.add_status(titlebar, "状态栏 | 标题栏")
                root.titlebar(titlebar)
                subframe = tk.Frame(root, relief=tk.FLAT, borderwidth=1)
                subwindow = dev.DevSubWindow(subframe, title="你好世界")
                statusbar.add_status(subwindow, "状态栏 | 子窗口")
                dragwidget = ttk.Button(subwindow, text="请拖动我")
                dev.DevToolTip(dragwidget, msg="就是一个普普通通的按钮")
                dragwidget.pack(fill=tk.BOTH, expand=tk.YES, padx=5, pady=5)
                dev.DevDrag(dragwidget, dragwidget)
                subwindow.place(x=5, y=5, width=260, height=260)
                subframe.pack(fill=tk.BOTH, expand=tk.YES, padx=15, pady=15)
                root.mainloop()


if __name__ == '__main__':
    root = devdemo()
    root.mainloop()
