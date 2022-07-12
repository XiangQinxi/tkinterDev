from tkdev import *


window = DevWindow()
date_label = tk.Label(window, text="请输入您活了多少年：")
date_label.pack(fill=tk.X, side=tk.TOP, padx=5, pady=5)
date_var = tk.StringVar()
date_entry = tk.Entry(window, textvariable=date_var, relief=tk.RIDGE)
date_entry.pack(fill=tk.X, side=tk.TOP, padx=5, pady=5)
old_label = tk.Label(window, text="您的年龄：")
old_label.pack(fill=tk.X, side=tk.TOP, padx=5, pady=5)
old_var = tk.StringVar()
old_entry = tk.Entry(window, textvariable=old_var, relief=tk.RIDGE)
old_entry.pack(fill=tk.X, side=tk.TOP, padx=5, pady=5)


def ok():
    old_var.set(date_entry.get())


ok_button = tk.Button(window, text="计算结果", relief=tk.RIDGE, borderwidth=1, background="#ffffff", command=ok)
ok_button.pack(fill=tk.X, side=tk.TOP, padx=5, pady=5)

window.title("实用的软件")
window.mainloop()