import ctypes
import os
import tkinter as tk
import tkinter.filedialog as tdialog
import tkinter.ttk as ttk
import tkinter.font
import datetime
from PIL import Image, ImageTk
import time
import pickle
import pystray
from infi.systray import SysTrayIcon

from messengerhandler import Handler as Handler
import tooltip
import Texts.text
import tkinterextension
import scheduler


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.data = self.load_data()
        self.settings_data = self.load_settings()
        self.handler = Handler()
        self.master = master
        # self.pack()

        self.save_cred = tk.BooleanVar()
        self.save_cred.set(True if not self.settings_data else self.settings_data["save_cred"])

        self.headless = tk.BooleanVar()
        self.headless.set(True if not self.settings_data or "headless" not in self.settings_data else
                          self.settings_data["headless"])

        self.method = tk.StringVar()

        self.iteration_value = tk.IntVar()
        self.iteration_value.set(
            1 if (not self.settings_data or "iteration" not in self.settings_data) else self.settings_data["iteration"])

        # scheduler
        self.hour = tk.IntVar()
        self.hour.set(datetime.datetime.now().strftime("%H"))
        self.min = tk.IntVar()
        self.min.set(datetime.datetime.now().strftime("%M"))

        self.menubar = tk.Menu(root)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        # self.filemenu.add_command(label="Undo", command=self.input_text.undo, accelerator="Ctrl+Z")
        # self.filemenu.add_command(label="Redo", accelerator="Ctrl+Y")
        self.filemenu.add_command(label="Read from file", command=self.read_input, accelerator="Ctrl+O")
        self.filemenu.add_command(label="Save credentials", command=self.save_data, accelerator="Ctrl+S")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Preferences", command=self.open_settings_, accelerator="Alt+P")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=root.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.actionmenu = tk.Menu(self.menubar, tearoff=0)
        # self.actionmenu.add_command(label="Send", underline=0, command=self.handle_messenger, accelerator="Ctrl+Enter")
        self.actionmenu.add_command(label="Senfd", underline=0,
                                    command=lambda: scheduler.check_alarm(root, self.handle_messenger,
                                                                          self.hour.get(), self.min.get()),
                                    accelerator="Ctrl+Enter")
        self.actionmenu.add_command(label="Autofill credentials", command=self.autofill_creds, accelerator="Alt+V")

        if not self.data or (self.settings_data and self.settings_data["save_cred"]) is False:
            self.actionmenu.entryconfig("Autofill credentials", state="disabled")
        self.menubar.add_cascade(label="Actions", menu=self.actionmenu)

        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="About...", command=lambda: tkinterextension.raise_frame(self.help_frame))
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        root.config(menu=self.menubar)

        self.login_frame = ttk.LabelFrame(text="Login")
        self.login_frame.grid(row=0, column=1, sticky="new")
        self.login_frame.grid_rowconfigure([0, 1, 2], weight=1, minsize=50)
        self.login_frame.grid_columnconfigure([0, 1], weight=1, minsize=130)

        self.email_label = ttk.Label(self.login_frame, text="Facebook email:")
        self.email_label.grid(row=0, column=0, sticky="w")
        self.email_entry = tkinterextension.LabelEntry(self.login_frame, label="test@email.com")
        self.email_entry.grid(row=0, column=1)

        self.password_label = ttk.Label(self.login_frame, text="Password:")
        self.password_label.grid(row=1, column=0, sticky="w")
        self.password_entry = ttk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1)

        self.link_label = ttk.Label(self.login_frame, text="Link:")
        self.link_label.grid(row=2, column=0, sticky="w")
        tooltip.CreateToolTip(self.link_label, text=Texts.text.link_tooltip)
        self.link_entry = tkinterextension.LabelEntry(self.login_frame, label="100000178957952")
        self.link_entry.grid(row=2, column=1)
        self.input_frame = ttk.LabelFrame(text="Text")
        self.input_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.input_frame.grid_rowconfigure([0], weight=1)
        self.input_frame.grid_columnconfigure([0], weight=1)

        self.input_label = ttk.Label(self.input_frame, text="Input")
        self.input_label.grid(row=0, column=0)
        tooltip.CreateToolTip(self.input_label, text=Texts.text.input_tooltip)
        self.input_text = tk.Text(self.input_frame, undo=True)
        self.input_text.insert("end", Texts.text.examplequote if not self.data or not self.data["email"] else self.data[
            "text"])
        self.input_text.grid(row=1, column=0)

        self.filemenu.add_command(label="Undo", command=self.input_text.edit_undo, accelerator="Ctrl+Z")
        self.filemenu.add_command(label="Redo", command=self.input_text.edit_redo, accelerator="Ctrl+Y")

        self.minimize = ttk.Button(self.input_frame, text="Minimize", command=self.hide_window)
        self.minimize.grid(row=2, column=0, sticky="e", padx=100)
        self.send_fb = ttk.Button(master=self.input_frame, text="Send now",
                                  command=self.handle_messenger)
        self.send_fb.grid(row=2, column=0, sticky="e")

        self.technical_frame = ttk.LabelFrame(text="Options")
        self.technical_frame.grid(row=1, column=1, sticky="new")
        self.technical_frame.grid_rowconfigure([0, 1], weight=1)
        self.technical_frame.grid_columnconfigure([0, 1], weight=1)

        self.method_label = ttk.Label(master=self.technical_frame, text="Send option:")
        self.method_label.grid(row=0, column=0, sticky="w")
        self.send_method = ttk.Combobox(master=self.technical_frame, width=10, state="readonly",
                                        textvariable=self.method)
        self.send_method['values'] = ('Plain text', 'Caption')
        self.send_method.current(0 if not self.settings_data or "method" not in self.settings_data
                                 else self.settings_data["method"])
        self.send_method.grid(row=0, column=1, sticky="w")

        self.iteration_label = ttk.Label(master=self.technical_frame, text="Iteration:")
        self.iteration_label.grid(row=1, column=0, sticky="w", pady=15)
        self.iteration_box = ttk.Spinbox(master=self.technical_frame, width=4, from_=1, to=100, wrap=True,
                                         textvariable=self.iteration_value)
        self.iteration_box.grid(row=1, column=1, sticky="w")

        self.scheduler_label = ttk.Label(master=self.technical_frame, text="Schedule:")
        self.scheduler_label.grid(row=2, column=0, sticky="w")
        # todo check possible bug that occur when 00 is passed instead of 0
        self.scheduler_hour = ttk.Spinbox(master=self.technical_frame, width=5, from_=0, to=23, increment=1,
                                          textvariable=self.hour, wrap=True)
        self.scheduler_hour.grid(row=2, column=1, sticky="w", padx=0)
        self.scheduler_minute = ttk.Spinbox(master=self.technical_frame, width=5, from_=0, to=59, increment=15,
                                            textvariable=self.min, wrap=True)
        self.scheduler_minute.grid(row=2, column=1, sticky="w", padx=55)
        self.scheduler_hourlabel = ttk.Label(self.technical_frame, text="Hours")
        self.scheduler_hourlabel.grid(row=2, column=1, sticky="w", padx=110)

        # self.cal = tkcalendar.DateEntry(self.technical_frame, width=10)
        # self.cal.grid(row=2, column=1, sticky="w")

        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        # menu popup
        self.popup = tk.Menu(self.input_text, tearoff=0)
        self.popup.add_command(label="Add divider", command=self.add_divider, accelerator="Alt+D")
        self.popup.add_command(label="Clear", command=self.clear_input, accelerator="Ctrl+Q")
        self.popup.add_separator()

        # help frame
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
        self.close_frame_button = ttk.Button(master=self.help_frame, text="Close",
                                             command=lambda: tkinterextension.lower_frame(self.help_frame))
        # self.close_frame_button = ttk.Button(master=self.help_frame, text="Close", command=lambda: tkinterextension.lower_frame(self.help_frame), style="Accentbutton")
        self.close_frame_button.grid(row=1, column=1)

        self.help_frame.lower()

        self.bind_keys()
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # to fix blurry text

    def bind_keys(self):
        self.input_text.bind("<Button-3>", self.menu_popup)

        # shortcuts
        root.bind('<Control-Return>', lambda e: self.handle_messenger())
        root.bind('<Control-o>', lambda e: self.read_input())
        root.bind('<Control-s>', lambda e: self.save_data())
        self.input_text.bind('<Alt-d>', lambda e: self.add_divider())
        self.input_text.bind('<Control-q>', lambda e: self.clear_input())

        root.bind('<Alt-p>', lambda e: self.open_settings_())
        root.bind('<Alt-v>', lambda e: self.autofill_creds())

    def open_settings_(self):
        settings = tk.Toplevel(root)
        settings.title("Settings")
        settings.geometry("550x400")

        save_cred_box = ttk.Checkbutton(master=settings, text="Save credentials", variable=self.save_cred)
        save_cred_box.grid(row=0, column=0, sticky="ews")
        tooltip.CreateToolTip(save_cred_box, text=Texts.text.save_cred_tooltip)

        headless_box = ttk.Checkbutton(settings, text="Headless browser", variable=self.headless)
        headless_box.grid(row=1, column=0, sticky="ews")
        tooltip.CreateToolTip(headless_box, text="When headless is applied, no browser with be shown during the autonomous process.")

        apply_button = ttk.Button(master=settings, text="Apply", command=self.apply_settings)
        apply_button.grid(row=2, column=0, sticky="ews")

    def menu_popup(self, event):
        try:
            self.popup.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup.grab_release()

    # add a divider symbol to the text, separating the text message
    def add_divider(self):
        self.input_text.insert(tk.INSERT, "\n$$\n\n")
        # print(self.input_text.index(tk.INSERT))

    def clear_input(self):
        self.input_text.delete('1.0', tk.END)

    def read_input(self):
        file = tdialog.askopenfile(parent=root, mode='rb', title='')
        if file is not None:
            data = file.read()
            file.close()
            self.input_text.delete('1.0', tk.END)
            # self.input_text.insert("end", data.decode("utf-8"))
            self.input_text.insert("end", data)

    def autofill_creds(self):
        if self.data is not False:
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert("end", self.data["email"])
            self.link_entry.delete(0, tk.END)
            self.link_entry.insert("end", self.data["link"])
        else:
            print("no previous credentials entered.")

    def hide_window(self):
        def clicked(icon=None):
            self.show_window()
            try:
                systray.shutdown()
            except:
                print()
                pass
        root.withdraw()
        menu_options = (("Show window", None, clicked),)
        systray = SysTrayIcon("Source/Resources/Icon/picturexviewer.ico", "Cappribot", menu_options, default_menu_index=0)
        systray.start()

    def show_window(self):
        root.deiconify()

    def handle_messenger(self):
        print("handling")
        self.save_data()
        # scheduler.alarm(root, print('hi'), self.hour.get(), self.min.get())
        self.handler.handle_message(self.input_text.get("1.0", tk.END), self.email_entry.get(),
                                    self.password_entry.get(),
                                    self.link_entry.get(), self.method.get(), self.iteration_value.get()
                                    , self.headless.get())

    def load_settings(self):
        if os.path.exists('Source/Resources/settings.txt'):
            try:
                with open('Source/Resources/settings.txt', 'r+b') as file:
                    return pickle.load(file)
            except EOFError:
                return {}
        else:
            return {}

    def apply_settings(self):
        if self.save_cred.get() is False:
            self.actionmenu.entryconfig("Autofill credentials", state="disabled")
            # not required to enable when changed to True, as no credentials will be saved before this
        self.save_settings()

    def save_settings(self):
        data = {'save_cred': self.save_cred.get(),
                'headless' : self.headless.get(),
                'iteration': self.iteration_value.get(),
                'method': self.send_method.current()}
        with open('Source/Resources/settings.txt', 'wb') as file:
            pickle.dump(data, file)

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
        self.save_settings()
        if self.save_cred.get() is False:
            data = {'email': False, 'link': False,
                    'text': self.input_text.get("1.0", tk.END)
                    }
        else:
            data = {'email': self.email_entry.get(), 'link': self.link_entry.get(),
                    'text': self.input_text.get("1.0", tk.END)
                    }
        with open('Source/Resources/save.txt', 'wb') as file:
            pickle.dump(data, file)


root = tk.Tk()
# ttk.Style().configure("TButton", padding=6, relief="flat", foreground="#E8E8E8", background="#292929")
default_font = tk.font.nametofont("TkDefaultFont")
# print(tk.font.families())
# default_font.configure(family="Garamond", size=13)
root.tk.call('source', 'Source/Resources/Style/azure.tcl')
root.tk.call("set_theme", "dark")
# style.configure("Accentbutton", foreground='white')
# style.configure("Togglebutton", foreground='white')
default_font.configure(size=11)
# root.geometry("1050x600")
root.title("Cappribot v0.2.0a")
root.iconphoto(False, tk.PhotoImage(file='Source/Resources/Icon/gradient_less_saturated.png'))
root.resizable(False, False)
app = Application(master=root)
app.mainloop()
