from typing import Optional
import ttkbootstrap as tb
import tkinter as tk
from tkinter import StringVar, messagebox as msgbox
from src.GUI.BaseView import BaseView
from src.GUI.utils import create_job_card_widget
from src.Services.SearchServices import SearchService
from src.Services.FavoritesServices import FavoritesService
from src.Services.BlacklistServices import BlacklistService

class SearchView(BaseView):
    def __init__(
        self,
        parent_frame_left: tk.Frame,
        parent_frame_right: tk.Frame,
        style_config: dict,
        search_service: SearchService,
        favorites_service: FavoritesService,
        blacklist_service: BlacklistService,
        add_link_button: tb.Button,
    ) -> None:
        
        super().__init__(parent_frame_left, parent_frame_right, style_config)

        self.search_service: SearchService = search_service
        self.favorites_service: FavoritesService = favorites_service
        self.blacklist_service: BlacklistService = blacklist_service

        self.current_selected_search: Optional[object] = None 
        self.add_link_button: tk.Button = add_link_button

        self.current_page: int = 0
        self.jobs_per_page: int = 25

        self._setup_ui()
        self.jobs_container.bind("<<BlacklistChanged>>", lambda e: self.render_current_page())

    def _setup_ui(self) -> None:
        """ 
            Renders the main UI components of the search view. 
            Left Frame: Search Jobs List
            Right Frame: Scrollable Jobs List + Pagination Frame 
        """

        # ==== Left: Search Listbox ====
        tk.Label(self.left_content_frame, text="Search List", padx=10, pady=10, 
                 font=(self.style_config['FONT_FAMILY'], self.style_config['FONT_SIZE'])).pack(fill=tk.X)
        self.search_listbox = tk.Listbox(self.left_content_frame, width=25, 
                                         font=(self.style_config['FONT_FAMILY'], self.style_config['FONT_SIZE'] - 4))
        self.search_listbox.bind("<<ListboxSelect>>", self.on_select_search)
        self.search_listbox.pack(fill=tk.BOTH, expand=True)
        self.update_search_listbox_display()

        # ==== Right: Content Area ====
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
        tb.Label(self.search_service_form, text="Frequency").pack(anchor="center")
        tb.Combobox(self.search_service_form, textvariable=self.search_freq,
                    values=["30 Minutes", "1 Hour", "6 Hours"], width=48, state="readonly").pack(anchor="center", pady=5)
        tb.Button(self.search_service_form, text="Add Search", bootstyle=tb.SUCCESS, 
                  command=self.callback_add_new_search).pack(anchor="center", pady=10)

        self.job_listbox_canvas = tk.Canvas(self.right_content_frame, bg="lightblue")
        self.job_listbox_scrollbar = tk.Scrollbar(self.right_content_frame, orient="vertical", command=self.job_listbox_canvas.yview)
        self.job_listbox_scrollable_frame = tk.Frame(self.job_listbox_canvas, bg="lightblue")

        self.job_listbox_scrollable_frame.bind("<Configure>", lambda e: self._configure_scroll_region(self.job_listbox_canvas))
        self.job_listbox_canvas.bind("<Enter>", lambda e: self._bind_to_mousewheel(e, self.job_listbox_canvas))
        self.job_listbox_canvas.bind("<Leave>", lambda e: self._unbind_from_mousewheel(e, self.job_listbox_canvas))

        self.frame_window_id = self.job_listbox_canvas.create_window((0, 0), window=self.job_listbox_scrollable_frame, anchor="nw")
        self.job_listbox_canvas.configure(yscrollcommand=self.job_listbox_scrollbar.set)
        self.job_listbox_canvas.bind("<Configure>", lambda e: self._configure_canvas_width(e, self.job_listbox_canvas, self.frame_window_id))

        self.jobs_container = tk.Frame(self.job_listbox_scrollable_frame, bg="lightblue")
        self.jobs_container.pack(fill="both", expand=True)

        self.pagination_frame = tb.Frame(self.job_listbox_scrollable_frame, padding=10, bootstyle="transparent")

        self.prev_button = tb.Button(self.pagination_frame, text="Previous", command=self.prev_page)
        self.page_label = tb.Label(self.pagination_frame, text="Page 1")
        self.next_button = tb.Button(self.pagination_frame, text="Next", command=self.next_page)

        self.prev_button.pack(side=tk.LEFT, padx=5)
        self.page_label.pack(side=tk.LEFT, padx=15)
        self.next_button.pack(side=tk.LEFT, padx=5)

        self.search_service_form.pack_forget()
        self.hide_job_listbox_display()

    def show_add_link_form_display(self, add_link_button_ref: tb.Button) -> None:
        self.hide_job_listbox_display()
        self.search_service_form.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        add_link_button_ref.config(text="x Close Form", bootstyle=tb.DANGER)

    def hide_add_link_form_display(self, add_link_button_ref: tb.Button) -> None:
        self.search_service_form.pack_forget()
        add_link_button_ref.config(text="+ Add Link", bootstyle=tb.PRIMARY)
        if self.current_selected_search:
            self.show_job_listbox_display()

    def show_job_listbox_display(self) -> None:
        self.search_service_form.pack_forget()
        self.job_listbox_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.job_listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.pagination_frame.pack(pady=10)

    def hide_job_listbox_display(self) -> None:
        self.job_listbox_canvas.pack_forget()
        self.job_listbox_scrollbar.pack_forget()
        self.pagination_frame.pack_forget()

    def callback_add_new_search(self) -> None:
        """
            + Called when a new search is added 

            Fetches all the input data: title, link, frequency.
            Transfers data to the SearchService.
        """

        title: str = self.search_service_title.get()
        link: str = self.search_service_link.get()
        freq_dict: dict[str, int] = {"30 Minutes": 30, "1 Hour": 60, "6 Hours": 360}
        
        selected_freq_str: str = self.search_freq.get()
        freq: Optional[int] = freq_dict.get(selected_freq_str)

        if not title or not link:
            msgbox.showerror("Error", "Title and Link are required.")
            return
        
        try:
            print(title, link, freq)
            new_search = self.search_service.add_search(title, link, freq)
        except Exception as e:
            msgbox.showerror("Error", f"Failed to add search: {e}")
            return

        if new_search:
            self.update_search_listbox_display()
            self.search_service_title.set("")
            self.search_service_link.set("")
            self.hide_add_link_form_display(self.add_link_button)
        else:
            msgbox.showerror("Error", "Failed to add search. Check logs.")

    def update_search_listbox_display(self) -> None:
        self.search_listbox.delete(0, tk.END)
        for search_item in self.search_service.searches:
            self.search_listbox.insert(tk.END, str(search_item))

    def on_select_search(self, event: tk.Event) -> None:
        """
            Called when a search in the left frame is selected.
        """

        selection = event.widget.curselection()
        if not selection:
            self.current_selected_search = None
            self.hide_job_listbox_display()
            return

        index: int = selection[0]
        self.current_selected_search = self.search_service.searches[index]
        self.current_page = 0

        self.search_service_form.pack_forget()
        self.show_job_listbox_display()
        self.render_current_page()

    def render_current_page(self) -> None:
        """
            Used for pagination rendering. Called by Next/Previous buttons. 
        """

        for widget in self.jobs_container.winfo_children():
            widget.destroy()

        jobs = [
            job
            for job in self.current_selected_search.get_jobs()
            if not self.blacklist_service.is_blacklisted(job)
        ]
        total_jobs: int = len(jobs)

        if total_jobs == 0:
            tk.Label(
                self.jobs_container,
                text="No jobs found for this search yet.",
                bg="lightblue",
                font=(self.style_config["FONT_FAMILY"], self.style_config["FONT_SIZE"]),
            ).pack(pady=20)
            self.pagination_frame.pack_forget()
            return

        start: int = self.current_page * self.jobs_per_page
        end: int = start + self.jobs_per_page
        jobs_to_display = jobs[start:end]

        for job_obj in jobs_to_display:
            card = create_job_card_widget(self.jobs_container, job_obj, self.favorites_service, self.blacklist_service)
            card.pack(fill="x", pady=5, padx=10)

        self.pagination_frame.pack(pady=10)
        self.pagination_frame.pack_configure(anchor="center")

        self.page_label.config(text=f"Page {self.current_page + 1}")

        if self.current_page == 0:
            self.prev_button.config(state="disabled")
        else:
            self.prev_button.config(state="normal")

        if end >= total_jobs:
            self.next_button.config(state="disabled")
        else:
            self.next_button.config(state="normal")

    def next_page(self) -> None:
        self.current_page += 1
        self.render_current_page()

    def prev_page(self) -> None:
        if self.current_page > 0:
            self.current_page -= 1
        self.render_current_page()