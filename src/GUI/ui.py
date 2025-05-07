import tkinter as tk
import tkinter.messagebox as msgbox
import ttkbootstrap as tb
import webbrowser
import pyperclip
import threading

from tkinter import StringVar
from src.GUI.config import FONT_FAMILY, FONT_SIZE, FONT_SIZE_BOLD
from src.Models.Search import Search
from src.Services.SearchServices import SearchService
from src.Models.job_model import Job

class JobUI:
    def __init__(self, root, search_service):
        self.root = root
        self.search_service = search_service
        self.static_selected_search = None
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

    

    # Custom Canvas Scrolling Functions - tkinter's listbox does not support custom cards inside so you have to build your own listbox and handle scrolling manually
    def _configure_scroll_region(self):
        """Sets the scrollable region of the canvas"""
        
        self.job_listbox_canvas.configure(scrollregion=self.job_listbox_canvas.bbox("all"))

    def _configure_canvas(self, event):
        """Adjusts the canvas width"""
        
        canvas_width = event.width
        self.job_listbox_canvas.itemconfig(self.frame_window_id, width=canvas_width)
    

    def _bind_to_mousewheel(self, event):
        """
            Generated with Claude 3.7

            Bind mousewheel events to canvas when mouse enters the canvas area
        """
        
        # Windows
        self.job_listbox_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        # Linux
        self.job_listbox_canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.job_listbox_canvas.bind_all("<Button-5>", self._on_mousewheel)
    
    def _unbind_from_mousewheel(self, event):
        """
            Generated with Claude 3.7

            Unbind mousewheel events when mouse leaves the canvas area 
        """
        
        # Windows
        self.job_listbox_canvas.unbind_all("<MouseWheel>")
        # Linux
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



    # Show/Hide logic

    # Toggling the Add Link top left button 
    def hide_add_link_form(self):
        self.search_service_form.pack_forget()
        self.add_link_button.config(text="+ Add Link", bootstyle=tb.PRIMARY, command=self.callback_add_search_form)
        self.right_frame.update()

    def show_add_link_form(self):
        self.search_service_form.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.add_link_button.config(text="x", bootstyle=tb.DANGER, command=self.hide_add_link_form)


    # Toggling the listbox when clicking on another menu
    def hide_job_listbox(self): 
        self.job_listbox_canvas.pack_forget()
        self.job_listbox_scrollbar.pack_forget()
        self.right_frame.update()

    def show_job_listbox(self):
        self.job_listbox_canvas.pack(side="left", fill="both", expand=True)
        self.job_listbox_scrollbar.pack(side="right", fill="y")


    # Callbacks used by buttons etc.
    def callback_add_search_form(self):
        self.show_add_link_form()
        self.hide_job_listbox()

    def callback_add_new_search(self):
        def update_search_service():
            for search in self.search_service.searches:
                search.job_search()

        self.search_service.add_search(self.search_service_title.get(), self.search_service_link.get(), self.search_platform.get(), self.search_freq.get())
        
        update_search_service()
        self.update_search_listbox()
        self.hide_add_link_form()



    def create_job_card(self, parent, ref_job):
        """
            Partly generated with Claude 3.7

            Given the input, it generates a card (frame) for the custom listbox (canvas).
        """

        title = ref_job.title
        company = ref_job.company
        link = ref_job.link

        card = tk.Frame(parent, padx=10, pady=10, relief="raised", borderwidth=1, bg="white")
        card.pack(fill=tk.X, expand=True, padx=5, pady=5)
        
        tk.Label(card, text=title, font=(FONT_FAMILY, FONT_SIZE_BOLD, 'bold'), anchor='w', bg="white", justify=tk.LEFT).pack(fill=tk.X)
        tk.Label(card, text=company, font=(FONT_FAMILY, FONT_SIZE - 6), anchor='w', bg="white", justify=tk.LEFT).pack(fill=tk.X)
        
        button_frame = tk.Frame(card, bg="white")

        save_btn = tb.Button(button_frame, text="Save")
        save_btn.config(command=lambda: self.save_job(ref_job, save_btn))
        if ref_job.saved:
            save_btn.config(text="Remove Saved", bootstyle=tb.DANGER)
        else:
            save_btn.config(text="Save", bootstyle=tb.PRIMARY)
        save_btn.pack(side="left", padx=(0, 5))

        apply_btn = tb.Button(button_frame, text="Apply")
        apply_btn.config(command=lambda: self.apply_to_job(ref_job, apply_btn))
        if ref_job.applied:
            apply_btn.config(text="Cancel Apply", bootstyle=tb.DANGER)
        else:
            apply_btn.config(text="Apply", bootstyle=tb.PRIMARY)
        apply_btn.pack(side="left", padx=(0, 5))
        
        tb.Button(button_frame, text="Open Link", command=lambda: self.open_link(link)).pack(side="left", padx=(0, 5))
        
        button_frame.pack(anchor='w', pady=(5, 0))
        
        return card

    def save_job(self, job, btn):
        print(f"Saved job {job}")
        job.saved = not job.saved

        if job.saved:
            btn.config(text="Remove Saved", bootstyle=tb.DANGER)
        else:
            btn.config(text="Save", bootstyle=tb.PRIMARY)
        

    def apply_to_job(self, job, btn):
        print(f"Applied to {job}")
        job.applied = not job.applied

        if job.applied:
            btn.config(text="Cancel Apply", bootstyle=tb.DANGER)
        else:
            btn.config(text="Apply", bootstyle=tb.PRIMARY)
        

    def update_search_listbox(self):
        self.search_listbox.delete(0, tk.END)
        for search in self.search_service.searches:
            self.search_listbox.insert(tk.END, str(search))  

    def update_job_listbox(self, selected_search):
        # Clear the cards in the UI
        for widget in self.job_listbox_scrollable_frame.winfo_children():
            widget.destroy()

        # Add the cards from the actual selected search
        for job in selected_search.get_jobs().values():
            card = self.create_job_card(self.job_listbox_scrollable_frame, job)
            card.pack(fill="x", pady=5, padx=10)

    def on_select_search(self, event):
        """
            Partly generated with ChatGPT

            Called when selecting a component in the Search Listbox. It then renders the job list corresponding to the selected Search in the custom listbox (canvas).
        """

        self.hide_add_link_form()
        self.show_job_listbox()

        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            self.static_selected_search = self.search_service.searches[index]

        self.update_job_listbox(self.static_selected_search)

    def open_link(self, url):
        """
            Generated with ChatGPT

            Open link function. It will open the link in the default browser. If no browser is set, it will copy the link to the clipboard using pyperclip.
        """

        try:
            webbrowser.get("windows-default").open_new_tab(url)
        except:
            pyperclip.copy(url)
            msgbox.showinfo("Link copied", f"Couldn't open browser.\nLink copied to clipboard:\n{url}")



class JobApp:
    def __init__(self, root):
        self.search_service = SearchService()
        self.ui = JobUI(root, self.search_service)
