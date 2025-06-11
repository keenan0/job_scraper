import ttkbootstrap as tb
import tkinter as tk
from tkinter import StringVar, messagebox as msgbox
from src.GUI.BaseView import BaseView
from src.GUI.utils import create_job_card_widget
from src.Services.SearchServices import SearchService

class SearchView(BaseView):
    def __init__(self, parent_frame_left, parent_frame_right, style_config, search_service, favorites_service):
        super().__init__(parent_frame_left, parent_frame_right, style_config)
        self.search_service: SearchService = search_service
        self.favorites_service = favorites_service
        self.current_selected_search = None

        self._setup_ui()

    def _setup_ui(self):
        # ==== Left: Search Listbox ====
        tk.Label(self.left_content_frame, text="Search List", padx=10, pady=10, 
                 font=(self.style_config['FONT_FAMILY'], self.style_config['FONT_SIZE'])).pack(fill=tk.X)
        self.search_listbox = tk.Listbox(self.left_content_frame, width=25, 
                                         font=(self.style_config['FONT_FAMILY'], self.style_config['FONT_SIZE'] - 4))
        self.search_listbox.bind("<<ListboxSelect>>", self.on_select_search)
        self.search_listbox.pack(fill=tk.BOTH, expand=True)
        self.update_search_listbox_display()

        # ==== Right: Content Area (Add Form or Job List) ====
        # Add Link Form (Inițial ascuns, dar creat)
        self.search_service_form = tb.Frame(self.right_content_frame, padding=5)
        self.search_service_title = StringVar()
        self.search_service_link = StringVar()
        self.search_platform = StringVar(value="LinkedIn")
        self.search_freq = StringVar(value="30 Minutes")

        tb.Label(self.search_service_form, text="Start a new search", 
                 font=(self.style_config['FONT_FAMILY'], 22)).pack(anchor="center", pady=25)
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
        tb.Button(self.search_service_form, text="Add Search", bootstyle=tb.SUCCESS, 
                  command=self.callback_add_new_search).pack(anchor="center", pady=10)

        # Custom Job Listbox for a selected Search
        self.job_listbox_canvas = tk.Canvas(self.right_content_frame, bg="lightblue")
        self.job_listbox_scrollbar = tk.Scrollbar(self.right_content_frame, orient="vertical", command=self.job_listbox_canvas.yview)
        self.job_listbox_scrollable_frame = tk.Frame(self.job_listbox_canvas, bg="lightblue")
        
        self.job_listbox_scrollable_frame.bind("<Configure>", lambda e: self._configure_scroll_region(self.job_listbox_canvas))
        self.job_listbox_canvas.bind("<Enter>", lambda e: self._bind_to_mousewheel(e, self.job_listbox_canvas))
        self.job_listbox_canvas.bind("<Leave>", lambda e: self._unbind_from_mousewheel(e, self.job_listbox_canvas))
        
        self.frame_window_id = self.job_listbox_canvas.create_window((0, 0), window=self.job_listbox_scrollable_frame, anchor="nw")
        self.job_listbox_canvas.configure(yscrollcommand=self.job_listbox_scrollbar.set)
        self.job_listbox_canvas.bind("<Configure>", lambda e: self._configure_canvas_width(e, self.job_listbox_canvas, self.frame_window_id))

        
        self.search_service_form.pack_forget()
        self.hide_job_listbox_display()


    def show_add_link_form_display(self, add_link_button_ref): 
        self.hide_job_listbox_display()
        self.search_service_form.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        add_link_button_ref.config(text="x Close Form", bootstyle=tb.DANGER)


    def hide_add_link_form_display(self, add_link_button_ref): 
        self.search_service_form.pack_forget()
        add_link_button_ref.config(text="+ Add Link", bootstyle=tb.PRIMARY)
        
        if self.current_selected_search:
            self.show_job_listbox_display()


    def show_job_listbox_display(self):
        self.search_service_form.pack_forget() 
        self.job_listbox_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.job_listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def hide_job_listbox_display(self):
        self.job_listbox_canvas.pack_forget()
        self.job_listbox_scrollbar.pack_forget()

    def callback_add_new_search(self):
       
        title = self.search_service_title.get()
        link = self.search_service_link.get()
        platform = self.search_platform.get()
        
        freq_dict = {
            "30 Minutes": 30,
            "1 Hour": 60,
            "6 Hours": 60 * 6
        }

        selected_freq_str = self.search_freq.get()
        freq = freq_dict.get(selected_freq_str)

        if not title or not link:
            msgbox.showerror("Error", "Title and Link are required.")
            return
        try:
            new_search = self.search_service.add_search(title, link, platform, freq)
        except Exception as e:
            msgbox.showerror("Error", f"Failed to add search: {e}")

        if new_search:
            self.update_search_listbox_display()
            # Gaseste butonul "+ Add Link" din JobUI si apeleaza hide pe el
            # Acest lucru e un pic un anti-pattern. Ideal, JobUI ar gestiona starea butonului.
            # Pentru moment, presupunem ca JobUI va apela hide_add_link_form_display
            # dupa ce acest callback se termina.
            # Sau, mai bine, JobUI ar trebui sa aiba o metoda care face asta.
            # job_ui_instance.toggle_add_search_form() # Exemplu
            msgbox.showinfo("Success", f"Search '{title}' added.")
            
            self.search_service_title.set("")
            self.search_service_link.set("")
        else:
            msgbox.showerror("Error", "Failed to add search. Check logs.")


    def update_search_listbox_display(self):
        self.search_listbox.delete(0, tk.END)
        for search_item in self.search_service.searches:
            self.search_listbox.insert(tk.END, str(search_item))  

    def on_select_search(self, event):
        selection = event.widget.curselection()
        if not selection:
            self.current_selected_search = None
            self.hide_job_listbox_display()
            return
        
        index = selection[0]
        self.current_selected_search = self.search_service.searches[index]

        # Asigura-te ca formularul de adaugare e ascuns si lista de joburi e vizibila
        # Acest lucru ar trebui gestionat de JobUI sau printr-o stare mai clara
        # De exemplu, JobUI.ensure_search_details_visible()
        self.search_service_form.pack_forget() # Ascunde explicit formularul
        self.show_job_listbox_display()

        for widget in self.job_listbox_scrollable_frame.winfo_children():
            widget.destroy()

        # Aici, get_jobs() ar trebui sa returneze o lista de obiecte Job
        # Asigura-te ca Search.get_jobs() returneaza Job-uri cu atributele title, company, link
        jobs_dict = self.current_selected_search.get_jobs() # Presupunem ca returneaza un dictionar de Job-uri
        if not jobs_dict:
             tk.Label(self.job_listbox_scrollable_frame, text="No jobs found for this search yet.", 
                      bg="lightblue", font=(self.style_config['FONT_FAMILY'], self.style_config['FONT_SIZE'])).pack(pady=20)

        for job_obj in jobs_dict: # Iteram prin valorile dictionarului (obiectele Job)
            card = create_job_card_widget(self.job_listbox_scrollable_frame, job_obj, self.favorites_service)
            card.pack(fill="x", pady=5, padx=10)
        
        self.job_listbox_canvas.yview_moveto(0) # Scroll la Inceput
        self._configure_scroll_region(self.job_listbox_canvas)