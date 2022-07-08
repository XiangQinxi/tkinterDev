import src.tkdev as dev
import tkinter as tk
import tkinter.ttk as ttk

root = dev.DevWindow()
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