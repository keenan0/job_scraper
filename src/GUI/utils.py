import ttkbootstrap as tb
import tkinter as tk
from src.GUI.config import FONT_FAMILY, FONT_SIZE, FONT_SIZE_BOLD
import webbrowser
import pyperclip
import tkinter.messagebox as msgbox

def open_link_handler(url):
    try:
        webbrowser.get("windows-default").open_new_tab(url)
    except Exception:
        pyperclip.copy(url)
        msgbox.showinfo("Link copied", f"Couldn't open browser.\nLink copied to clipboard:\n{url}")


def create_job_card_widget(parent, job, favorites_service, on_remove_callback=None):
    card = tk.Frame(parent, padx=10, pady=10, relief="raised", borderwidth=1, bg="white")
    
    tk.Label(card, text=job.title, font=(FONT_FAMILY, FONT_SIZE_BOLD, 'bold'), anchor='w', bg="white", justify=tk.LEFT).pack(fill=tk.X)
    tk.Label(card, text=job.company, font=(FONT_FAMILY, FONT_SIZE - 6), anchor='w', bg="white", justify=tk.LEFT).pack(fill=tk.X)
    
    button_frame = tk.Frame(card, bg="white")
    
    if on_remove_callback: 
        tk.Button(button_frame, text="Remove", padx=10, command=lambda j=job: on_remove_callback(j)).pack(side="left", padx=(0, 5))
    else: 
        tk.Button(button_frame, text="Save", padx=10, command=lambda j=job: favorites_service.add_favorite_job(j)).pack(side="left", padx=(0, 5))
        
    tk.Button(button_frame, text="Open Link", command=lambda link=job.link: open_link_handler(link), padx=10).pack(side="left")
    button_frame.pack(anchor='w', pady=(5, 0))
    
    return card
