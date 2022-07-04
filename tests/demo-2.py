import tkdev as dev
import tkinter as tk


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("300x300")
    subwindow = dev.DevSubWindow(root,title="DevSubWindow")
    subwindow.place(x=5, y=5, width=290, height=290)

    root.mainloop()