import ttkbootstrap as tb
import tkinter as tk
from typing import Any


class BaseView:
    def __init__(
        self,
        parent_frame_left: tb.Frame | tk.Widget,
        parent_frame_right: tb.Frame | tk.Widget,
        style_config: dict[str, Any],
    ) -> None:
        """
            Initialize BaseView with left and right parent frames and style configuration.
        """
        self.parent_frame_left = parent_frame_left
        self.parent_frame_right = parent_frame_right
        self.style_config = style_config

        self.left_content_frame = tb.Frame(self.parent_frame_left)
        self.right_content_frame = tb.Frame(self.parent_frame_right)

    def show(self) -> None:
        self.left_content_frame.pack(fill=tk.BOTH, expand=True)
        self.right_content_frame.pack(fill=tk.BOTH, expand=True)

    def hide(self) -> None:
        self.left_content_frame.pack_forget()
        self.right_content_frame.pack_forget()

    def _configure_scroll_region(self, canvas: tk.Canvas) -> None:
        """
            Configure the scrollable region of a canvas widget.
        """

        canvas.configure(scrollregion=canvas.bbox("all"))

    def _configure_canvas_width(
        self, event: tk.Event, canvas: tk.Canvas, frame_window_id: int
    ) -> None:
        """
            Adjust the width of the canvas window item to match the canvas width.
        """

        canvas_width = event.width
        canvas.itemconfig(frame_window_id, width=canvas_width)

    def _bind_to_mousewheel(self, event: tk.Event, canvas: tk.Canvas) -> None:
        canvas.bind_all(
            "<MouseWheel>", lambda e, c=canvas: self._on_mousewheel(e, c)
        )
        canvas.bind_all(
            "<Button-4>", lambda e, c=canvas: self._on_mousewheel(e, c)
        )
        canvas.bind_all(
            "<Button-5>", lambda e, c=canvas: self._on_mousewheel(e, c)
        )

    def _unbind_from_mousewheel(self, event: tk.Event, canvas: tk.Canvas) -> None:
        canvas.unbind_all("<MouseWheel>")
        canvas.unbind_all("<Button-4>")
        canvas.unbind_all("<Button-5>")

    def _on_mousewheel(self, event: tk.Event, canvas: tk.Canvas) -> None:
        """
            Handle mouse wheel scrolling event.
        """
        
        if hasattr(event, "num"):
            if event.num == 5:
                canvas.yview_scroll(1, "units")
            elif event.num == 4:
                canvas.yview_scroll(-1, "units")
        elif hasattr(event, "delta"):
            if event.delta < 0:
                canvas.yview_scroll(1, "units")
            elif event.delta > 0:
                canvas.yview_scroll(-1, "units")