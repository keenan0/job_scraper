import ttkbootstrap as tb
import tkinter as tk

class BaseView:
    def __init__(self, parent_frame_left, parent_frame_right, style_config):
        self.parent_frame_left = parent_frame_left
        self.parent_frame_right = parent_frame_right
        self.style_config = style_config 
        
        self.left_content_frame = tb.Frame(self.parent_frame_left)
        self.right_content_frame = tb.Frame(self.parent_frame_right)

    def show(self):
        self.left_content_frame.pack(fill=tk.BOTH, expand=True)
        self.right_content_frame.pack(fill=tk.BOTH, expand=True)

    def hide(self):
        self.left_content_frame.pack_forget()
        self.right_content_frame.pack_forget()

    def _configure_scroll_region(self, canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def _configure_canvas_width(self, event, canvas, frame_window_id):
        canvas_width = event.width
        canvas.itemconfig(frame_window_id, width=canvas_width)

    def _bind_to_mousewheel(self, event, canvas):
        canvas.bind_all("<MouseWheel>", lambda e, c=canvas: self._on_mousewheel(e, c))
        canvas.bind_all("<Button-4>", lambda e, c=canvas: self._on_mousewheel(e, c))
        canvas.bind_all("<Button-5>", lambda e, c=canvas: self._on_mousewheel(e, c))
    
    def _unbind_from_mousewheel(self, event, canvas):
        canvas.unbind_all("<MouseWheel>")
        canvas.unbind_all("<Button-4>")
        canvas.unbind_all("<Button-5>")
    
    def _on_mousewheel(self, event, canvas):
        if event.num == 5 or event.delta < 0:
            canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            canvas.yview_scroll(-1, "units")