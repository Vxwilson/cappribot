import tkinter as tk
import tkinter.ttk as ttk

class LabelEntry(tk.Entry):
    def __init__(self, master=None, label="Search", **kwargs):
        ttk.Entry.__init__(self, master, **kwargs)
        self.label = label
        self.on_exit()
        self.bind('<FocusIn>', self.on_entry)
        self.bind('<FocusOut>', self.on_exit)

    def on_entry(self, event=None):
        if self.get() == self.label:
            self.delete(0, tk.END)
            self.config(foreground='white')

    def on_exit(self, event=None):
        if not self.get():
            self.insert(0, self.label)
            self.config(foreground='grey')


def raise_frame(frame):
    frame.lift()


def lower_frame(frame):
    frame.lower()
