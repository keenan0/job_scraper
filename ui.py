import ttkbootstrap as tb
import tkinter as tk
from tkinter import StringVar
from job_model import Job
from scraper import scrape_jobs
import threading
import webbrowser
import tkinter.messagebox as msgbox
import pyperclip
from config import FONT_FAMILY, FONT_SIZE, FONT_SIZE_BOLD

class JobManager:
    def __init__(self):
        self.jobs = []
        self.selected_job = None

    def add_jobs(self, jobs):
        self.jobs.extend(jobs)

    def select_job(self, idx):
        if idx is None:
            self.selected_job = None
        else:
            self.selected_job = self.jobs[idx]

    def clear(self):
        self.jobs = []
        self.selected_job = None



class JobUI:
    def __init__(self, root, job_manager):
        self.root = root
        self.job_manager = job_manager
        self.root.title("MDS - Job Scraper")
        
        self.style = tb.Style('flatly')
        self.style.configure('.', font=(FONT_FAMILY, FONT_SIZE))
        self.style.configure('TButton', font=(FONT_FAMILY, FONT_SIZE_BOLD, 'bold'))
        self.style.configure('TLabel', font=(FONT_FAMILY, FONT_SIZE_BOLD))

        """Main Frame - (Input Field + Search Button)"""
        self.frame = tb.Frame(root, padding=5)
        self.frame.pack(fill=tk.BOTH, expand=False)

        self.url_var = StringVar()
        tb.Entry(self.frame, textvariable=self.url_var, width=60).pack(side=tk.LEFT, padx=5)
        tb.Button(self.frame, text="Search", bootstyle=tb.PRIMARY, style="TButton",command=self.on_search).pack(side=tk.LEFT)

        """End Main Frame"""

        """Horizontal Search Container - Job List + Job Controls"""
        self.container = tb.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.container.pack(fill=tk.BOTH, expand=True)

        self.job_listbox = tk.Listbox(self.container, width=25, font=(FONT_FAMILY, FONT_SIZE))
        self.job_listbox.bind("<<ListboxSelect>>", self.on_select)
        self.container.add(self.job_listbox)

        """Job Details + Controls"""
        self.job_detail_frame = tb.Frame(self.container, padding=10)
        self.container.add(self.job_detail_frame)

        self.title_label = tb.Label(self.job_detail_frame, text="", font=(FONT_FAMILY, 18, "bold"))
        self.title_label.pack(anchor="w", pady=(0, 5))

        self.company_label = tb.Label(self.job_detail_frame, text="", font=(FONT_FAMILY, FONT_SIZE))
        self.company_label.pack(anchor="w", pady=(0, 5))

        self.link_frame = tb.Frame(self.job_detail_frame)
        self.link_frame.pack(anchor="w", pady=(0, 10))

        self.link_button = tb.Button(self.link_frame, text="See Job", bootstyle="info", command=lambda: None)

        self.description_text = tk.Text(self.job_detail_frame, wrap=tk.WORD, font=(FONT_FAMILY, FONT_SIZE_BOLD), height=10, width=60)
        self.description_text.bind("<Key>", lambda e: "break")
        self.hide_description()
        """End Job Details + Controls"""
        """End Horizontal Search Container"""

    def update_job_list(self):
        """Actualizează lista de joburi din UI."""
        self.job_listbox.delete(0, tk.END)
        for job in self.job_manager.jobs:
            self.job_listbox.insert(tk.END, job.title)

    def on_search(self):
        url = self.url_var.get()
        self.job_manager.clear()  # Golește lista de joburi
        self.update_job_list()

        self.hide_description()
        self.description_text.delete(1.0, tk.END)
        self.description_text.pack_forget()
        threading.Thread(target=self.scrape_thread, args=(url,)).start()

    def scrape_thread(self, url):
        """Scrapează joburile și le adaugă în JobManager."""
        jobs = scrape_jobs(url)
        job_objects = [Job(job.title, job.company, job.location, job.link, job.description) for job in jobs]

        self.job_manager.add_jobs(job_objects)
        self.update_job_list()

    def on_select(self, event):
        idx = self.job_listbox.curselection()
        if not idx:
            self.hide_description()
            return
        job = self.job_manager.jobs[idx[0]]
        self.job_manager.select_job(idx[0])

        self.title_label.config(text=job.title)
        self.company_label.config(text=job.company)
        self.link_button.config(command=lambda: self.open_link(job.link))
        if not self.link_button.winfo_ismapped():
            self.link_button.pack()

        self.description_text.pack(anchor="w", fill=tk.BOTH, expand=True)
        self.description_text.delete(1.0, tk.END)
        self.description_text.insert(tk.END, job.description)

    def open_link(self, url):
        try:
            webbrowser.get("windows-default").open_new_tab(url)
        except:
            pyperclip.copy(url)
            msgbox.showinfo("Link copied", f"Couldn't open browser.\nLink copied to clipboard:\n{url}")

    def hide_description(self):
        self.title_label.config(text="")
        self.company_label.config(text="")
        self.link_button.pack_forget()
        self.description_text.delete(1.0, tk.END)
        self.job_detail_frame.pack_forget()

    def show_description(self):
        self.job_detail_frame.pack(fill=tk.BOTH, expand=True)



class JobApp:
    def __init__(self, root):
        self.job_manager = JobManager()
        self.ui = JobUI(root, self.job_manager)
