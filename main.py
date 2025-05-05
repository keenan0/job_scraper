import ttkbootstrap as tb
from ui import JobApp

if __name__ == '__main__':
    root = tb.Window()
    root.geometry("1000x700")
    
    root.resizable(False, False)
    root.maxsize(1000, 700)
    root.minsize(1000, 700)

    app = JobApp(root)
    root.mainloop()