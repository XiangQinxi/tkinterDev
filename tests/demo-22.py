import tkdev as dev
import tkinter as tk
import tkinter.ttk as ttk

if __name__ == '__main__':
    root = tk.Tk() 
    root.geometry("500x500")
    button = ttk.Button(root)
    button.place(x=10, y=10, width=480, height=480)
    dev.DevDrag(button, button)
    dev.DevResize(widget=button)
    root.mainloop()