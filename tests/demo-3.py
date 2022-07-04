import tkdev as dev

if __name__ == '__main__':
    root = dev.DevWindow()
    root.geometry("300x300")
    titlebar = dev.DevTitleBar(root, iswindow=True, window=root)
    root.titlebar(titlebar)
    root.mainloop()