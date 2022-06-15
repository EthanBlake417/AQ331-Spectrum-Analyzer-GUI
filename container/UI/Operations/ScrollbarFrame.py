import tkinter as tk


class ScrollbarFrame(tk.Frame):
    """
    Extends class tk.Frame to support a scrollable Frame
    This class is independent from the widgets to be scrolled and
    can be used to replace a standard tk.Frame
    """
    def __init__(self, parent, width=350, height=350, **kwargs):
        tk.Frame.__init__(self, parent, width=350, height=350, **kwargs)

        # The Scrollbar, layout to the right
        vsb = tk.Scrollbar(self, orient="vertical")
        vsb.pack(side="right", fill="y")
        self.width = width
        self.height = height
        # The Canvas which supports the Scrollbar Interface, layout to the left
        self.canvas = tk.Canvas(self, borderwidth=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Bind the Scrollbar to the self.canvas Scrollbar Interface
        self.canvas.configure(yscrollcommand=vsb.set)
        vsb.configure(command=self.canvas.yview)

        # The Frame to be scrolled, layout into the canvas
        # All widgets to be scrolled have to use this Frame as parent
        self.scrolled_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrolled_frame, anchor="nw")

        # Configures the scrollregion of the Canvas dynamically
        self.scrolled_frame.bind("<Configure>", self.on_configure)

    def on_configure(self, event):
        """Set the scroll region to encompass the scrolled frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"), width=self.width, height=self.height)