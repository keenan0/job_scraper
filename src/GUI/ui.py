import ttkbootstrap as tb
import tkinter as tk
from tkinter import StringVar
import threading
import webbrowser
import tkinter.messagebox as msgbox
import pyperclip
from config import FONT_FAMILY, FONT_SIZE, FONT_SIZE_BOLD
from src.Models.Search import Search

class SearchService:
    def __init__(self):
        self.searches = [] 

    def add_search(self, title, link, platform, frequency):
        self.searches.extend([Search(title, link, platform, frequency)])



class JobUI:
    def __init__(self, root, search_service):
        self.root = root
        self.search_service = search_service
        self.root.title("MDS - Job Scraper")
        
        self.style = tb.Style('darkly')
        self.style.configure('.', font=(FONT_FAMILY, FONT_SIZE))
        self.style.configure('TButton', font=(FONT_FAMILY, FONT_SIZE_BOLD, 'bold'))
        self.style.configure('TLabel', font=(FONT_FAMILY, FONT_SIZE_BOLD))

        # ==== Top Frame ====
        self.frame = tb.Frame(root, padding=10)
        self.frame.pack(fill=tk.X)
        self.add_link_button = tb.Button(self.frame, text="+ Add Link", width=12, command=self.show_add_link_form)
        self.add_link_button.pack(side=tk.LEFT)

        # ==== Horizontal Container ====
        self.container = tb.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.container.pack(fill=tk.BOTH, expand=True)

        # ==== Left: Listbox ====
        self.left_frame = tb.Frame(self.container, padding=10)

        self.label_search_list = tk.Label(self.left_frame, text="Search List", padx=10, pady=10, font=(FONT_FAMILY, FONT_SIZE))
        self.label_search_list.pack(fill=tk.BOTH)

        self.search_listbox = tk.Listbox(self.left_frame, width=25, font=(FONT_FAMILY, FONT_SIZE - 6))
        self.search_listbox.bind("<<ListboxSelect>>", self.on_select_search)
        self.search_listbox.pack(fill=tk.BOTH, expand=True)

        self.container.add(self.left_frame)

        # ==== Right: Job Details + Add Link Form ====
        self.right_frame = tb.Frame(self.container, padding=10)
        self.container.add(self.right_frame)

        # Add Link Form (Hidden by Default)
        self.search_service_form = tb.Frame(self.right_frame, padding=5)
        self.search_service_title = StringVar()
        self.search_service_link = StringVar()
        self.search_platform = StringVar(value="LinkedIn")
        self.search_freq = StringVar(value="30 Minutes")

        tb.Label(self.search_service_form, text="Start a new search", font=(FONT_FAMILY, 22)).pack(anchor="center", pady=25)

        tb.Label(self.search_service_form, text="Job Title").pack(anchor="center")
        tb.Entry(self.search_service_form, textvariable=self.search_service_title, width=50).pack(anchor="center", pady=5)

        tb.Label(self.search_service_form, text="Job Link").pack(anchor="center")
        tb.Entry(self.search_service_form, textvariable=self.search_service_link, width=50).pack(anchor="center", pady=5)

        tb.Label(self.search_service_form, text="Platform").pack(anchor="center")
        tb.Combobox(self.search_service_form, textvariable=self.search_platform,
                    values=["LinkedIn", "eJobs", "Hipo"], width=48, state="readonly").pack(anchor="center", pady=5)

        tb.Label(self.search_service_form, text="Frequency").pack(anchor="center")
        tb.Combobox(self.search_service_form, textvariable=self.search_freq,
                    values=["30 Minutes", "1 Hour", "6 Hours"], width=48, state="readonly").pack(anchor="center", pady=5)

        tb.Button(self.search_service_form, text="Add Search", bootstyle=tb.SUCCESS, command=lambda: (self.search_service.add_search(self.search_service_link.get(), self.search_freq.get(), self.search_platform.get(), self.search_service_title.get()),self.update_search_listbox(),self.hide_add_link_form())).pack(anchor="center", pady=10)

        # Job Details Section
        self.job_detail_frame = tb.Frame(self.right_frame, padding=10)
        self.job_detail_frame.pack(fill=tk.BOTH, expand=True)

        self.title_label = tb.Label(self.job_detail_frame, text="", font=(FONT_FAMILY, 18, "bold"))
        self.title_label.pack(anchor="w", pady=(0, 5))

        self.company_label = tb.Label(self.job_detail_frame, text="", font=(FONT_FAMILY, FONT_SIZE))
        self.company_label.pack(anchor="w", pady=(0, 5))

        self.link_frame = tb.Frame(self.job_detail_frame)
        self.link_frame.pack(anchor="w", pady=(0, 10))

        self.link_button = tb.Button(self.link_frame, text="See Job", bootstyle="info", command=lambda: None)
        self.favorite_button = tb.Button(self.link_frame, text="Save Job", bootstyle="danger", command=lambda: None)

        self.description_text = tk.Text(self.job_detail_frame, wrap=tk.WORD, font=(FONT_FAMILY, FONT_SIZE_BOLD),
                                        height=10, width=60)
        self.description_text.bind("<Key>", lambda e: "break")

        self.hide_description()

    def update_search_listbox(self):
        self.search_listbox.delete(0, tk.END)
        for search in self.search_service.searches:
            self.search_listbox.insert(tk.END, str(search))  

    def hide_add_link_form(self):
        self.search_service_form.pack_forget()
        self.add_link_button.config(text="+ Add Link", bootstyle=tb.PRIMARY, command=self.show_add_link_form)

    def show_add_link_form(self):
        self.search_service_form.pack(fill=tk.BOTH, expand=False, padx=10, pady=10)
        self.add_link_button.config(text="x", bootstyle=tb.DANGER, command=self.hide_add_link_form)

    def on_search(self):
        url = self.url_var.get()
        self.update_job_list()

        self.hide_description()
        self.description_text.delete(1.0, tk.END)
        self.description_text.pack_forget()
        threading.Thread(target=self.scrape_thread, args=(url,)).start()

    def scrape_thread(self, url):
        # jobs = scrape_jobs(url)
        # job_objects = [Job(job.title, job.company, job.location, job.link, job.description) for job in jobs]

        # self.search_service.add_search(job_objects)
        # self.update_job_list()
        pass

    def on_select_search(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            selected_search = self.search_service.searches[index]

        print(selected_search)

    # def on_select(self, event):
    #     idx = self.job_listbox.curselection()
    #     if not idx:
    #         self.hide_description()
    #         return
    #     job = self.search_service.searches[idx[0]]
    #     self.search_service.select_job(idx[0])

    #     self.title_label.config(text=job.title)
    #     self.company_label.config(text=job.company)
    #     self.link_button.config(command=lambda: self.open_link(job.link))
    #     if not self.link_button.winfo_ismapped():
    #         self.link_button.pack(side=tb.LEFT, padx=5)

    #     self.favorite_button.config(command=lambda: self.toggle_saved(self.job_manager.selected_job))
    #     self.favorite_button.config(text=f"{'Save Job' if not self.job_manager.selected_job.saved else 'Remove Job'}")
    #     self.favorite_button.pack(side=tb.LEFT, padx=5)
        
    #     self.description_text.pack(anchor="w", fill=tk.BOTH, expand=True)
    #     self.description_text.delete(1.0, tk.END)
    #     self.description_text.insert(tk.END, job.description)

    def toggle_saved(self, current_job):
        current_job.saved = not current_job.saved
        self.job_manager.save_job(current_job)
        self.favorite_button.config(text=f"{'Save Job' if not current_job.saved else 'Remove Job'}")

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
        self.favorite_button.pack_forget()
        self.description_text.delete(1.0, tk.END)
        self.job_detail_frame.pack_forget()

    def show_description(self):
        self.job_detail_frame.pack(fill=tk.BOTH, expand=True)



class JobApp:
    def __init__(self, root):
        self.search_service = SearchService()
        self.ui = JobUI(root, self.search_service)
