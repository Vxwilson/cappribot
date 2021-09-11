import ctypes
import os
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font
import pickle
from messengerhandler import Handler as Handler
from tooltip import ToolTip
import tooltip
import Texts.text
import tkinterextension


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.data = self.load_data()
        self.handler = Handler()
        self.master = master
        # self.pack()
        style = self.darkstyle()

        self.save_cred = tk.BooleanVar()
        self.save_cred.set(True if not self.data else self.data["save_cred"])

        self.menubar = tk.Menu(root)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        # self.filemenu.add_command(label="New")
        # self.filemenu.add_command(label="Open")
        # self.filemenu.add_command(label="Save")

        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=root.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.actionmenu = tk.Menu(self.menubar, tearoff=0)
        self.actionmenu.add_command(label="Autofill credentials", command=self.autofill_creds)
        if self.data["email"] is False:
            self.actionmenu.entryconfig("Autofill credentials", state="disabled")
        # self.actionmenu.add_checkbutton(label="Save credentials", onvalue=1, offvalue=0, variable=self.save_cred)
        self.menubar.add_cascade(label="Actions", menu=self.actionmenu)

        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="About...", command=lambda: tkinterextension.raise_frame(self.help_frame))
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        root.config(menu=self.menubar)

        self.login_frame = ttk.LabelFrame(text="Login")
        self.login_frame.grid(row=0, column=0, sticky="nsew")
        self.login_frame.grid_rowconfigure([0, 1, 2], weight=1)
        self.login_frame.grid_columnconfigure([0, 1, 2], weight=1)

        self.email_label = ttk.Label(self.login_frame, text="Facebook email:")
        self.email_label.grid(row=0, column=0)
        self.email_entry = tkinterextension.LabelEntry(self.login_frame, label="test@email.com")
        self.email_entry.grid(row=0, column=1)

        self.password_label = ttk.Label(self.login_frame, text="Password:")
        self.password_label.grid(row=1, column=0)
        self.password_entry = ttk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1)

        self.link_label = ttk.Label(self.login_frame, text="Link:")
        self.link_label.grid(row=2, column=0)
        tooltip.CreateToolTip(self.link_label, text=Texts.text.link_tooltip)
        self.link_entry = tkinterextension.LabelEntry(self.login_frame, label="100000178957952")
        self.link_entry.grid(row=2, column=1)
        self.input_frame = ttk.LabelFrame(text="Text")
        self.input_frame.grid(row=1, column=0, sticky="nsew")
        self.input_frame.grid_rowconfigure([0], weight=1)
        self.input_frame.grid_columnconfigure([0], weight=1)

        self.input_label = ttk.Label(self.input_frame, text="Input")
        self.input_label.grid(row=0, column=0)
        tooltip.CreateToolTip(self.input_label, text=Texts.text.input_tooltip)
        self.input_text = tk.Text(self.input_frame)
        self.input_text.insert("end", Texts.text.examplequote if not self.data["email"] else self.data["text"])
        self.input_text.grid(row=1, column=0)

        self.send_fb = ttk.Button(master=self.input_frame, text="Send to Messenger",
                                  command=self.handle_messenger)
        self.send_fb.grid(row=2, column=0)

        self.technical_frame = ttk.LabelFrame(text="Options")
        self.technical_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")
        self.technical_frame.grid_rowconfigure(0, weight=1)
        self.technical_frame.grid_columnconfigure(0, weight=1)

        self.save_cred_box = ttk.Checkbutton(master=self.technical_frame, text="Save credentials", variable=self.save_cred)
        self.save_cred_box.grid(row=0, column=0, sticky="n")
        tooltip.CreateToolTip(self.save_cred_box, text=Texts.text.save_cred_tooltip)
        self.quit = ttk.Button(master=self.technical_frame, text="QUIT",
                               command=self.master.destroy, style="Accentbutton")
        # self.quit.grid(row=0, column=0, sticky="s")

        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        ##help frame
        self.help_frame = ttk.LabelFrame(text="Help", width=500, height=300)
        self.help_frame.grid_propagate(False)
        self.login_frame.grid_rowconfigure([0, 1], weight=1)
        self.login_frame.grid_columnconfigure(0, weight=1)
        self.help_frame.grid(row=0, column=0)
        self.help_label = ttk.Label(self.help_frame, text="""
        Cappribot version 0.1.0
        refer to GitHub readme.md for more information
        """)
        self.help_label.grid(row=0, column=0)
        self.close_frame_button = ttk.Button(master=self.help_frame, text="Close", command=lambda: tkinterextension.lower_frame(self.help_frame), style="Accentbutton")
        self.close_frame_button.grid(row=1, column=1)

        self.help_frame.lower()

        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # to fix blurry text

    def darkstyle(self):
        ''' Return a dark style to the window'''

        style = ttk.Style(self)
        self.tk.call('source', 'Source/Resources/Style/azure dark.tcl')
        style.theme_use('azure')
        style.configure("Accentbutton", foreground='white')
        style.configure("Togglebutton", foreground='white')
        return style

    def autofill_creds(self):
        if self.data is not False:
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert("end", self.data["email"])
            self.link_entry.delete(0, tk.END)
            self.link_entry.insert("end", self.data["link"])
        else:
            print("no previous credentials entered.")
    def handle_messenger(self):
        # self.send_fb["state"] = "disabled"
        self.save_data()
        self.handler.send_message(self.input_text.get("1.0", tk.END), self.email_entry.get(), self.password_entry.get(),
                                  self.link_entry.get())
        # self.send_fb["state"] = "normal"

    def load_data(self):
        if os.path.exists('Source/Resources/save.txt'):
            try:
                with open('Source/Resources/save.txt', 'r+b') as file:
                    return pickle.load(file)
            except EOFError:
                return {}
        else:
            return {}

    def save_data(self):
        print(self.save_cred.get())
        if self.save_cred.get() is False:
            data = {'email': False, 'link': False,
                    'text': self.input_text.get("1.0", tk.END),
                    'save_cred': self.save_cred.get()}
        else:
            data = {'email': self.email_entry.get(), 'link': self.link_entry.get(),
                    'text': self.input_text.get("1.0", tk.END),
                    'save_cred': self.save_cred.get()}
        with open('Source/Resources/save.txt', 'wb') as file:
            pickle.dump(data, file)

root = tk.Tk()
# ttk.Style().configure("TButton", padding=6, relief="flat", foreground="#E8E8E8", background="#292929")
default_font = tk.font.nametofont("TkDefaultFont")
# print(tk.font.families())
default_font.configure(family="Garamond", size=13)
root.geometry("1366x768")
root.title("Cappribot v0.1.5a")
root.iconphoto(False, tk.PhotoImage(file='Source/Resources/Icon/gradient_less_saturated.png'))
root.resizable(False, False)
app = Application(master=root)
app.mainloop()

