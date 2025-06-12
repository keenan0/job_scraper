import ttkbootstrap as tb
from src.GUI.ui import JobApp
import os

if __name__ == '__main__':
    root = tb.Window()
    root.geometry("1000x700")

    app_data_dir = os.path.join(os.path.expanduser("~"), ".job_scraper")
    os.makedirs(app_data_dir, exist_ok=True)

    root.resizable(False, False)
    root.maxsize(1000, 700)
    root.minsize(1000, 700)

    app = JobApp(root)
    root.mainloop()