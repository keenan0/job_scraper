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
from Models.Search import Search

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
        
        #self.style = tb.Style('darkly') # flatly
        self.style = tb.Style()
        self.style.configure('.', font=(FONT_FAMILY, FONT_SIZE))
        self.style.configure('TButton', font=(FONT_FAMILY, FONT_SIZE_BOLD, 'bold'))
        self.style.configure('TLabel', font=(FONT_FAMILY, FONT_SIZE_BOLD))

        # ==== Top Frame ====
        self.frame = tb.Frame(root, padding=10)
        self.frame.pack(fill=tk.X)
        self.add_link_button = tb.Button(self.frame, text="+ Add Link", width=12, command=self.callback_add_search_form)
        self.add_link_button.pack(side=tk.LEFT)

        # ==== Horizontal Container ====
        self.container = tb.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.container.pack(fill=tk.BOTH, expand=True)

        # ==== Left: Listbox ====
        self.left_frame = tb.Frame(self.container, padding=10)

        self.label_search_list = tk.Label(self.left_frame, text="Search List", padx=10, pady=10, font=(FONT_FAMILY, FONT_SIZE))
        self.label_search_list.pack(fill=tk.BOTH)

        self.search_listbox = tk.Listbox(self.left_frame, width=25, font=(FONT_FAMILY, FONT_SIZE - 4))
        self.search_listbox.bind("<<ListboxSelect>>", self.on_select_search)
        self.search_listbox.pack(fill=tk.BOTH, expand=True)

        self.container.add(self.left_frame)

        # ==== Right Frame ====
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

        tb.Button(self.search_service_form, text="Add Search", bootstyle=tb.SUCCESS, command=self.callback_add_new_search).pack(anchor="center", pady=10)

        # Custom Job Listbox for a selected Search
        self.job_listbox_canvas = tk.Canvas(self.right_frame, bg="lightblue")
        self.job_listbox_scrollbar = tk.Scrollbar(self.right_frame, orient="vertical", command=self.job_listbox_canvas.yview)

        # Configurăm canvas-ul să ocupe tot spațiul disponibil
        self.job_listbox_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.job_listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Frame-ul scrollabil trebuie să aibă lățimea configurabilă pentru a se extinde
        self.job_listbox_scrollable_frame = tk.Frame(self.job_listbox_canvas, bg="lightblue")
        self.job_listbox_scrollable_frame.bind("<Configure>", lambda e: self._configure_scroll_region())

        # Adăugăm event-urile pentru mouse wheel scroll
        self.job_listbox_canvas.bind("<Enter>", self._bind_to_mousewheel)
        self.job_listbox_canvas.bind("<Leave>", self._unbind_from_mousewheel)

        # Creăm fereastra în canvas și obținem ID-ul pentru a-l putea actualiza mai târziu
        self.frame_window_id = self.job_listbox_canvas.create_window(
            (0, 0), 
            window=self.job_listbox_scrollable_frame, 
            anchor="nw",
        )

        self.job_listbox_canvas.configure(yscrollcommand=self.job_listbox_scrollbar.set)

        # Adăugăm un event pentru când canvas-ul își schimbă dimensiunea
        self.job_listbox_canvas.bind("<Configure>", self._configure_canvas)

    

    # Other Utility Functions
    def _configure_scroll_region(self):
        """Actualizează regiunea de scroll a canvas-ului pentru a include tot conținutul frame-ului"""
        self.job_listbox_canvas.configure(scrollregion=self.job_listbox_canvas.bbox("all"))

    def _configure_canvas(self, event):
        """Ajustează lățimea ferestrei create în canvas pentru a se potrivi cu lățimea canvas-ului"""
        # Setează lățimea frame-ului scrollabil la lățimea canvas-ului
        canvas_width = event.width
        self.job_listbox_canvas.itemconfig(self.frame_window_id, width=canvas_width)
    

    def _bind_to_mousewheel(self, event):
        print("ENTERED")
        """Bind mousewheel events to canvas when mouse enters the canvas area"""
        # Pentru Windows
        self.job_listbox_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        # Pentru Linux
        self.job_listbox_canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.job_listbox_canvas.bind_all("<Button-5>", self._on_mousewheel)
    
    def _unbind_from_mousewheel(self, event):
        print("EXITED")
        """Unbind mousewheel events when mouse leaves the canvas area"""
        # Pentru Windows
        self.job_listbox_canvas.unbind_all("<MouseWheel>")
        # Pentru Linux
        self.job_listbox_canvas.unbind_all("<Button-4>")
        self.job_listbox_canvas.unbind_all("<Button-5>")
    
    def _on_mousewheel(self, event):
        """Handle mousewheel scrolling"""
        # Pentru Windows
        if event.num == 5 or event.delta < 0:
            self.job_listbox_canvas.yview_scroll(1, "units")
        # Pentru Linux
        elif event.num == 4 or event.delta > 0:
            self.job_listbox_canvas.yview_scroll(-1, "units")



    # SHOW/HIDE
    def hide_add_link_form(self):
        self.search_service_form.pack_forget()
        self.add_link_button.config(text="+ Add Link", bootstyle=tb.PRIMARY, command=self.callback_add_search_form)
        self.right_frame.update()

    def show_add_link_form(self):
        self.search_service_form.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.add_link_button.config(text="x", bootstyle=tb.DANGER, command=self.hide_add_link_form)



    def hide_job_listbox(self): 
        self.job_listbox_canvas.pack_forget()
        self.job_listbox_scrollbar.pack_forget()
        self.right_frame.update()


    def show_job_listbox(self):
        self.job_listbox_canvas.pack(side="left", fill="both", expand=True)
        self.job_listbox_scrollbar.pack(side="right", fill="y")


    # UTILITY

    def callback_add_search_form(self):
        self.show_add_link_form()
        self.hide_job_listbox()

    def callback_add_new_search(self):
        self.search_service.add_search(self.search_service_link.get(), self.search_freq.get(), self.search_platform.get(), self.search_service_title.get())
        self.update_search_listbox()

        self.hide_add_link_form()

    def create_job_card(self, parent, title, company, location, link):
        # Creăm un frame pentru card care va ocupa toată lățimea disponibilă
        card = tk.Frame(parent, padx=10, pady=10, relief="raised", borderwidth=1, bg="white")
        
        # Folosim pack cu fill=tk.X pentru a ocupa toată lățimea disponibilă
        card.pack(fill=tk.X, expand=True, padx=5, pady=5)
        
        # Adăugăm elementele cardului
        tk.Label(card, text=title, font=('Arial', 14, 'bold'), anchor='w', bg="white", justify=tk.LEFT).pack(fill=tk.X)
        tk.Label(card, text=company, font=('Arial', 12), anchor='w', bg="white", justify=tk.LEFT).pack(fill=tk.X)
        tk.Label(card, text=location, font=('Arial', 12, 'italic'), anchor='w', bg="white", justify=tk.LEFT).pack(fill=tk.X)
        
        # Butoanele
        button_frame = tk.Frame(card, bg="white")
        tk.Button(button_frame, text="Salvează", padx=10).pack(side="left", padx=(0, 5))
        tk.Button(button_frame, text="Deschide job", command=lambda: self.open_link(link), padx=10).pack(side="left")
        button_frame.pack(anchor='w', pady=(5, 0))
        
        return card

    def show_search_jobs(self):
        self.search_service_form.pack_forget()
        self.job_detail_frame.pack(fill=tb.BOTH)

    def update_search_listbox(self):
        self.search_listbox.delete(0, tk.END)
        for search in self.search_service.searches:
            self.search_listbox.insert(tk.END, str(search))  

    def scrape_thread(self, url):
        pass

    def on_select_search(self, event):
        self.hide_add_link_form()
        self.show_job_listbox()

        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            selected_search = self.search_service.searches[index]

        for job in selected_search.get_jobs():
            card = self.create_job_card(self.job_listbox_scrollable_frame, job.title, job.company, job.location, job.link)
            card.pack(fill="x", pady=5, padx=10)

        print(selected_search.get_jobs())

    def open_link(self, url):
        try:
            webbrowser.get("windows-default").open_new_tab(url)
        except:
            pyperclip.copy(url)
            msgbox.showinfo("Link copied", f"Couldn't open browser.\nLink copied to clipboard:\n{url}")



class JobApp:
    def __init__(self, root):
        self.search_service = SearchService()
        self.ui = JobUI(root, self.search_service)
