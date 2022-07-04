import tkdev as dev
import tkinter as tk

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("500x500")
    drag_widget = tk.Label(root, background="black", foreground="white", text="Hello DevDrag")
    drag_widget.pack(fill=tk.BOTH, expand=tk.YES)
    dev.DevDrag(drag_widget, drag_widget)
    root.mainloop()