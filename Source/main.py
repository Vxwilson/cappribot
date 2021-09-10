import ctypes
import random
import asyncio
import tkinter as tk
import tkinter.ttk as ttk
from messengerhandler import Handler as Handler


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.handler = Handler()
        self.master = master
        # self.pack()
        self.create_widgets()
        style = self.darkstyle()

        self.login_frame = ttk.LabelFrame(text="Login")
        self.login_frame.grid(row=0, column=0, sticky="nsew")
        self.login_frame.grid_rowconfigure([0, 1, 2], weight=1)
        self.login_frame.grid_columnconfigure([0, 1, 2], weight=1)

        self.email_label = ttk.Label(self.login_frame, text="Facebook email:")
        self.email_label.grid(row=0, column=0)
        self.email_entry = ttk.Entry(self.login_frame)
        self.email_entry.insert("end", 'veixhen@hotmail.com')
        self.email_entry.grid(row=0, column=1)

        self.password_label = ttk.Label(self.login_frame, text="Password:")
        self.password_label.grid(row=1, column=0)
        self.password_entry = ttk.Entry(self.login_frame)
        self.password_entry.grid(row=1, column=1)

        self.link_label = ttk.Label(self.login_frame, text="Link:")
        self.link_label.grid(row=2, column=0)
        self.link_entry = ttk.Entry(self.login_frame)
        self.link_entry.insert("end", "100000178957922")
        self.link_entry.grid(row=2, column=1)

        self.input_frame = ttk.LabelFrame(text="Text")
        self.input_frame.grid(row=1, column=0, sticky="nsew")
        self.input_frame.grid_rowconfigure([0], weight=1)
        self.input_frame.grid_columnconfigure([0], weight=1)

        self.input_label = ttk.Label(self.input_frame, text="Input")
        self.input_label.grid(row=0, column=0)
        self.input_text = tk.Text(self.input_frame)
        self.input_text.grid(row=1, column=0)

        self.send_fb = ttk.Button(master=self.input_frame, text="Send to Messenger",
                                  command=self.handle_messenger)
        self.send_fb.grid(row=2, column=0)

        self.technical_frame = ttk.LabelFrame(text="Options")
        self.technical_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")
        self.technical_frame.grid_rowconfigure(0, weight=1)
        self.technical_frame.grid_columnconfigure(0, weight=1)

        self.quit = ttk.Button(master=self.technical_frame, text="QUIT",
                               command=self.master.destroy, style="Accentbutton")
        self.quit.grid(row=0, column=0, sticky="s")

        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # to fix blurry text

    def create_widgets(self):
        string = ""

    def darkstyle(self):
        ''' Return a dark style to the window'''

        style = ttk.Style(self)
        self.tk.call('source', 'Source/Resources/Style/azure dark.tcl')
        style.theme_use('azure')
        style.configure("Accentbutton", foreground='white')
        style.configure("Togglebutton", foreground='white')
        return style

    def handle_messenger(self):
        self.send_fb["state"] = "disabled"
        self.handler.send_message(self.input_text.get("1.0", tk.END), self.email_entry.get(), self.password_entry.get(), self.link_entry.get())
        self.send_fb["state"] = "normal"


root = tk.Tk()
# ttk.Style().configure("TButton", padding=6, relief="flat", foreground="#E8E8E8", background="#292929")
root.geometry("1000x563")
root.title("Wallpaper Changer")
root.iconphoto(False, tk.PhotoImage(file='Source/Resources/Icon/gradient_less_saturated.png'))
app = Application(master=root)
app.mainloop()
