import ttkbootstrap as tb
import tkinter as tk
from tkinter import StringVar
import threading
import webbrowser
import tkinter.messagebox as msgbox
import pyperclip
import src
from src.GUI.config import FONT_FAMILY, FONT_SIZE, FONT_SIZE_BOLD
from src.Models.Search import Search
from src.Models.job_model import Job
from src.Services.SearchServices import SearchService
from src.Services.FavoritesServices import FavoritesService
from src.GUI.FavoritesView import FavoritesView
from src.GUI.SearchView import SearchView

class JobUI:
    def __init__(self, root, search_service, favorites_service):
        self.root = root
        self.search_service = search_service
        self.favorites_service = favorites_service
        self.root.title("MDS - Job Scraper")
        
        self.style = tb.Style() # Sau 'darkly' etc.
        self.style_config = {
            'FONT_FAMILY': FONT_FAMILY, 
            'FONT_SIZE': FONT_SIZE,
            'FONT_SIZE_BOLD': FONT_SIZE_BOLD
        }
        self.style.configure('.', font=(self.style_config['FONT_FAMILY'], self.style_config['FONT_SIZE']))
        self.style.configure('TButton', font=(self.style_config['FONT_FAMILY'], self.style_config['FONT_SIZE_BOLD'], 'bold'))
        self.style.configure('AppNav.TButton', font=(self.style_config['FONT_FAMILY'], self.style_config['FONT_SIZE'])) 
        self.style.configure('TLabel', font=(self.style_config['FONT_FAMILY'], self.style_config['FONT_SIZE_BOLD']))

        self.current_view = None
        self._setup_main_layout()
        self._setup_views()
        
        self.show_search_view() # Afiseaza view-ul de search initial

    def _setup_main_layout(self):
        # ==== Top Navigation Frame ====
        self.nav_frame = tb.Frame(self.root, padding=(10,10,10,0))
        self.nav_frame.pack(fill=tk.X)

        self.search_view_button = tb.Button(self.nav_frame, text="Search", width=12, style='AppNav.TButton', command=self.show_search_view)
        self.search_view_button.pack(side=tk.LEFT, padx=(0,5))
        
        self.favorites_view_button = tb.Button(self.nav_frame, text="Favorites", width=12, style='AppNav.TButton', command=self.show_favorites_view)
        self.favorites_view_button.pack(side=tk.LEFT, padx=(0,5))

        # Butonul "+ Add Link" este specific view-ului de Search, dar controlat de aici pentru vizibilitate globala
        self.add_link_button = tb.Button(self.nav_frame, text="+ Add Link", width=12, style='AppNav.TButton', command=self.toggle_add_search_form)
        self.add_link_button.pack(side=tk.LEFT, padx=(0,5))


        # ==== Horizontal Container pentru conținut ====
        self.container = tb.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.container.pack(fill=tk.BOTH, expand=True, pady=(5,0))

        
        self.left_pane_content_frame = tb.Frame(self.container, padding=10)
        self.container.add(self.left_pane_content_frame, weight=1) # weight pentru resizing

        self.right_pane_content_frame = tb.Frame(self.container, padding=10)
        self.container.add(self.right_pane_content_frame, weight=3) # weight pentru resizing

    def _setup_views(self):
        self.search_view_instance = SearchView(self.left_pane_content_frame, self.right_pane_content_frame, 
                                               self.style_config, self.search_service, self.favorites_service)
        self.favorites_view_instance = FavoritesView(self.left_pane_content_frame, self.right_pane_content_frame,
                                                     self.style_config, self.favorites_service)

    def _switch_view(self, new_view):
        if self.current_view:
            self.current_view.hide()
        
        self.current_view = new_view
        self.current_view.show()

        
        if self.current_view == self.search_view_instance:
            self.add_link_button.pack(side=tk.LEFT, padx=(0,5)) 
            
            if not self.search_view_instance.search_service_form.winfo_ismapped():
                 self.add_link_button.config(text="+ Add Link", bootstyle=tb.PRIMARY)
            else:
                 self.add_link_button.config(text="x Close Form", bootstyle=tb.DANGER)

        else:
            self.add_link_button.pack_forget() 


    def show_search_view(self):
        self._switch_view(self.search_view_instance)
        self.search_view_button.config(bootstyle=tb.PRIMARY)
        self.favorites_view_button.config(bootstyle=tb.SECONDARY)


    def show_favorites_view(self):
        self._switch_view(self.favorites_view_instance)
        self.favorites_view_button.config(bootstyle=tb.PRIMARY)
        self.search_view_button.config(bootstyle=tb.SECONDARY)
       
        if self.search_view_instance.search_service_form.winfo_ismapped():
            self.search_view_instance.hide_add_link_form_display(self.add_link_button)


    def toggle_add_search_form(self):
        
        if self.current_view == self.search_view_instance:
            if self.search_view_instance.search_service_form.winfo_ismapped():
                self.search_view_instance.hide_add_link_form_display(self.add_link_button)
            else:
                self.search_view_instance.show_add_link_form_display(self.add_link_button)
        
        else:
            self.show_search_view()



class JobApp:
    def __init__(self, root):
        self.search_service = SearchService()
        self.favorites_service = FavoritesService()
        self.ui = JobUI(root, self.search_service,self.favorites_service)

