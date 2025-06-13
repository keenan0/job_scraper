import ttkbootstrap as tb
import tkinter as tk
from tkinter import StringVar, messagebox as msgbox
from typing import Optional, Any
from src.GUI.BaseView import BaseView
from src.GUI.utils import create_job_card_widget
from src.Services.FavoritesServices import FavoritesService

class FavoritesView(BaseView):
    def __init__(
        self,
        parent_frame_left: tk.Frame,
        parent_frame_right: tk.Frame,
        style_config: dict[str, Any],
        favorites_service: FavoritesService
    ) -> None:
        super().__init__(parent_frame_left, parent_frame_right, style_config)
        
        self._setup_ui()
        self.favorites_service = favorites_service
        self.refresh_favorites_display()

    def _setup_ui(self) -> None:
        """ 
            Renders the main UI components of the favories view. 
        """
        
        tk.Label(
            self.left_content_frame,
            text="Favorite Jobs",
            padx=10,
            pady=10,
            font=(self.style_config['FONT_FAMILY'], self.style_config['FONT_SIZE'])
        ).pack(fill=tk.X)

        self.fav_job_listbox_canvas: tk.Canvas = tk.Canvas(self.right_content_frame, bg="lightyellow")
        self.fav_job_listbox_scrollbar: tk.Scrollbar = tk.Scrollbar(
            self.right_content_frame, orient="vertical", command=self.fav_job_listbox_canvas.yview
        )
        self.fav_job_listbox_scrollable_frame: tk.Frame = tk.Frame(self.fav_job_listbox_canvas, bg="lightyellow")

        self.fav_job_listbox_scrollable_frame.bind(
            "<Configure>", lambda e: self._configure_scroll_region(self.fav_job_listbox_canvas)
        )
        self.fav_job_listbox_canvas.bind(
            "<Enter>", lambda e: self._bind_to_mousewheel(e, self.fav_job_listbox_canvas)
        )
        self.fav_job_listbox_canvas.bind(
            "<Leave>", lambda e: self._unbind_from_mousewheel(e, self.fav_job_listbox_canvas)
        )

        self.fav_frame_window_id: int = self.fav_job_listbox_canvas.create_window(
            (0, 0), window=self.fav_job_listbox_scrollable_frame, anchor="nw"
        )
        self.fav_job_listbox_canvas.configure(yscrollcommand=self.fav_job_listbox_scrollbar.set)
        self.fav_job_listbox_canvas.bind(
            "<Configure>", lambda e: self._configure_canvas_width(e, self.fav_job_listbox_canvas, self.fav_frame_window_id)
        )

        self.fav_job_listbox_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.fav_job_listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def refresh_favorites_display(self) -> None:
        for widget in self.fav_job_listbox_scrollable_frame.winfo_children():
            widget.destroy()

        favorite_jobs = self.favorites_service.get_all_favorites()
        if not favorite_jobs:
            tk.Label(
                self.fav_job_listbox_scrollable_frame,
                text="No favorite jobs yet. Save some!",
                bg="lightyellow",
                font=(self.style_config['FONT_FAMILY'], self.style_config['FONT_SIZE'])
            ).pack(pady=20)
        else:
            for job in favorite_jobs:
                card = create_job_card_widget(
                    self.fav_job_listbox_scrollable_frame,
                    job,
                    self.favorites_service,
                    on_remove_callback=self.remove_job_from_favorites_ui
                )
                card.pack(fill="x", pady=5, padx=10)

        self.fav_job_listbox_canvas.yview_moveto(0)
        self._configure_scroll_region(self.fav_job_listbox_canvas)

    def remove_job_from_favorites_ui(self, job_to_remove: Any) -> None:
        if self.favorites_service.remove_favorite_job(job_to_remove):
            self.refresh_favorites_display()
            #msgbox.showinfo("Removed", f"Job '{job_to_remove.title}' removed from favorites.")
        else:
            msgbox.showerror("Error", f"Could not remove job '{job_to_remove.title}'.")

    def show(self) -> None:
        super().show()
        self.refresh_favorites_display()