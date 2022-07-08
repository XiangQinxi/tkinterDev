from src.tkdev import *


Window = DevWindow()
Docs = DevDocs(Window)
Docs.add_docs("Hello", "")
Docs.pack(fill=tk.BOTH, expand=tk.YES)
Window.mainloop()