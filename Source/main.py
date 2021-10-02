import ctypes
import os
import tkinter as tk
import tkinter.filedialog as tdialog
import tkinter.ttk as ttk
import tkinter.font
import tkinter.messagebox
import datetime
import pickle
from infi.systray import SysTrayIcon
from functools import partial
import pkg_resources

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
        self.link_data = self.load_link()
        self.handler = Handler()
        self.scheduler = scheduler.Scheduler(root, self.handle_messenger)
        self.schedules = self.scheduler.load_schedules()
        self.master = master
        # self.pack()

        self.save_cred = tk.BooleanVar()
        self.save_cred.set(True if not self.settings_data else self.settings_data["save_cred"])

        self.headless = tk.BooleanVar()
        self.headless.set(True if not self.settings_data or "headless" not in self.settings_data else
                          self.settings_data["headless"])
        self.minimize_radio = tk.IntVar()
        self.minimize_radio.set(1 if not self.settings_data or "minimize_radio" not in self.settings_data else
                                self.settings_data["minimize_radio"])

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
        self.filemenu.add_command(label="Minimize", command=self.hide_window, accelerator="Ctrl+H")
        # self.filemenu.add_command(label="Save credentials", command=self.save_data, accelerator="Ctrl+S")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Preferences", command=self.open_settings_, accelerator="Alt+P")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=root.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.actionmenu = tk.Menu(self.menubar, tearoff=0)
        self.actionmenu.add_command(label="New task", command=lambda: self.new_instant_task(), accelerator="Control+N")
        self.actionmenu.add_command(label="Schedule new task", command=lambda: self.new_schedule(),
                                    accelerator="Control+Shift+N")
        self.actionmenu.add_command(label="Set credentials", command=self.set_credentials, accelerator="Alt+C")
        self.actionmenu.add_command(label="Add Link", command=self.add_link, accelerator="Control+L")
        self.menubar.add_cascade(label="Actions", menu=self.actionmenu)

        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="About...", command=lambda: tkinterextension.raise_frame(self.help_frame))
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        root.config(menu=self.menubar)

        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        # menu popup
        # self.popup = tk.Menu(self.input_text, tearoff=0)
        # self.popup.add_command(label="Add divider", command=self.add_divider, accelerator="Alt+D")
        # self.popup.add_command(label="Clear", command=self.clear_input, accelerator="Ctrl+Q")
        # self.popup.add_separator()

        # help frame
        self.help_frame = ttk.LabelFrame(text="Help", width=400)
        # self.help_frame.grid_propagate(False)
        self.help_frame.grid(row=0, column=0)
        self.help_label = ttk.Label(self.help_frame, text="""
        Cappribot version 0.1.0
        refer to GitHub readme.md for more information
        """)
        # self.help_label.grid(row=0, column=0)
        self.help_info_text = """
Cappribot version 0.2.5 \n
        
Before using the program, add your Facebook Messenger credentials through Actions > Set Credentials.
To send a instant text, go to Actions > New Task.
To schedule tasks, go to Actions > Schedule New Task.

Iterations refer to the amount of times a text is sent to the recipient. 
Text formatting:
using '<>' in the text gives the index of the text, e.g. "No.<>" becomes "No.1"
adding '&&' splits the text at that point to separate the text messages sent.
Be aware that for scheduled tasks to work, the program must either be open, or in a minimized state!  
    
Please refer to GitHub readme.md for more information.
created by vxix in 2021.
        """
        self.help_info = tk.Text(self.help_frame, width=55, height=20)
        self.help_info.insert('end', self.help_info_text)
        self.help_info.configure(state='disabled')
        self.help_info.grid(row=0, column=0, sticky="ew")

        # self.close_frame_button = ttk.Button(master=self.help_frame, text="Close",
        #                                      command=lambda: tkinterextension.lower_frame(self.help_frame))
        # # self.close_frame_button = ttk.Button(master=self.help_frame, text="Close", command=lambda: tkinterextension.lower_frame(self.help_frame), style="Accentbutton")
        # self.close_frame_button.grid(row=1, column=0)

        # self.help_frame.lower()

        self.scheduled_frame = ttk.LabelFrame(text="Schedules", width=300, height=250)
        self.scheduled_frame.grid_propagate(False)
        self.scheduled_frame.grid(row=0, column=1)
        self.update_schedule()
        # self.help_label = ttk.Label(self.scheduled_frame, text="Scheduled tasks")
        # self.help_label.grid(row=0, column=0)

        self.bind_keys()
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # to fix blurry text

        root.protocol('WM_DELETE_WINDOW', self.override_close)

    def bind_keys(self):
        # self.input_text.bind("<Button-3>", self.menu_popup)

        # shortcuts
        root.bind('<Control-Return>', lambda e: self.scheduler.try_start_alarm(root, self.handle_messenger,
                                                                               self.hour.get(), self.min.get()), )
        root.bind('<Control-o>', lambda e: self.read_input())
        # root.bind('<Control-s>', lambda e: self.save_data())
        root.bind('<Control-n>', lambda e: self.new_instant_task())
        root.bind('<Control-l>', lambda e: self.add_link())
        root.bind('<Control-Shift-N>', lambda e: self.new_schedule())
        root.bind('<Control-h>', lambda e: self.hide_window())
        # self.input_text.bind('<Alt-d>', lambda e: self.add_divider())
        # self.input_text.bind('<Control-q>', lambda e: self.clear_input())

        root.bind('<Alt-p>', lambda e: self.open_settings_())
        root.bind('<Alt-c>', lambda e: self.set_credentials())

    def open_settings_(self):
        settings = tk.Toplevel(root)
        settings.title("Settings")
        settings.minsize(550, 350)

        save_cred_box = ttk.Checkbutton(master=settings, text="Save credentials", variable=self.save_cred)
        save_cred_box.grid(row=0, column=0, sticky="ews")
        tooltip.CreateToolTip(save_cred_box, text=Texts.text.save_cred_tooltip)

        headless_box = ttk.Checkbutton(settings, text="Headless browser", variable=self.headless)
        headless_box.grid(row=1, column=0, sticky="ews")
        tooltip.CreateToolTip(headless_box,
                              text="When headless is applied, no browser with be shown during the autonomous process.")

        minimize_option_label = ttk.Label(settings, text="Close program prompt")
        minimize_option_label.grid(row=2, column=0, sticky="ewn", pady=20)
        minimize_option_radio = ttk.Radiobutton(settings, text="Always ask", variable=self.minimize_radio,
                                                value=1)
        minimize_option_radio2 = ttk.Radiobutton(settings, text="Minimize", variable=self.minimize_radio,
                                                 value=2)
        minimize_option_radio3 = ttk.Radiobutton(settings, text="Close", variable=self.minimize_radio,
                                                 value=3)
        minimize_option_radio.grid(row=2, column=0, sticky="ewn", pady=40)
        minimize_option_radio2.grid(row=2, column=0, sticky="ewn", pady=70)
        minimize_option_radio3.grid(row=2, column=0, sticky="ewn", pady=100)

        clear_creds = ttk.Button(settings, text="Clear credentials", command=self.clear_creds)
        clear_creds.grid(row=3, column=0, sticky="ews")
        apply_button = ttk.Button(master=settings, text="Apply",
                                  command=lambda: [self.apply_settings(), settings.destroy()])
        apply_button.grid(row=4, column=0, sticky="ews")

    def set_credentials(self):

        def save_data():
            self.save_settings()
            data = {'email': email_entry.get(), 'link': link_entry.get(),
                    'password': password_entry.get()
                    # 'text': input_text.get("1.0", tk.END)
                    }
            with open('Source/Resources/save.txt', 'wb') as file:
                pickle.dump(data, file)
            self.data = self.load_data()

        cred_window = tk.Toplevel(root)
        cred_window.title("Save credentials")
        cred_window.minsize(350, 250)

        login_frame = ttk.LabelFrame(cred_window, text="Login")
        login_frame.grid(row=0, column=0, sticky="new")
        login_frame.grid_rowconfigure([0, 1, 2], weight=1, minsize=50)
        login_frame.grid_columnconfigure([0, 1], weight=1, minsize=130)

        email_label = ttk.Label(login_frame, text="Facebook email:")
        email_label.grid(row=0, column=0, sticky="w")
        email_entry = tkinterextension.LabelEntry(login_frame, label="example@email.com")
        email_entry.grid(row=0, column=1)

        password_label = ttk.Label(login_frame, text="Password:")
        password_label.grid(row=1, column=0, sticky="w")
        password_entry = tkinterextension.LabelEntry(login_frame, show="*", label="12345678")
        password_entry.grid(row=1, column=1)

        link_label = ttk.Label(login_frame, text="Default recipient (link):")
        link_label.grid(row=2, column=0, sticky="w")
        tooltip.CreateToolTip(link_label, text=Texts.text.link_tooltip)
        link_entry = tkinterextension.LabelEntry(login_frame, label="100000178957952")
        link_entry.grid(row=2, column=1)

        apply_button = ttk.Button(master=cred_window, text="Save", command=lambda: [save_data(),
                                                                                    cred_window.destroy()])
        apply_button.grid(row=2, column=0, sticky="ew")

        # autofill previous credentials
        if bool(self.data):
            email_entry.delete(0, tk.END)
            email_entry.insert("end", self.data["email"])
            password_entry.delete(0, tk.END)
            password_entry.insert("end", self.data["password"])
            link_entry.delete(0, tk.END)
            link_entry.insert("end", self.data["link"])

    def add_link(self):
        add_link_window = tk.Toplevel(root)
        add_link_window.title("Add link")
        add_link_window.minsize(350, 250)

        link_frame = ttk.LabelFrame(add_link_window, text="")
        link_frame.grid(row=0, column=0, sticky="new")
        link_frame.grid_rowconfigure([0, 1, 2], weight=1, minsize=50)
        link_frame.grid_columnconfigure([0, 1], weight=1, minsize=130)

        link_label = ttk.Label(link_frame, text="Link:")
        link_label.grid(row=0, column=0, sticky="w")
        link_entry = tkinterextension.LabelEntry(link_frame, label="100000178957952")
        link_entry.grid(row=0, column=1)

        name_label = ttk.Label(link_frame, text="Name:")
        name_label.grid(row=1, column=0, sticky="w")
        name_entry = tkinterextension.LabelEntry(link_frame, label="John")
        name_entry.grid(row=1, column=1)

        apply_button = ttk.Button(master=add_link_window, text="Save", command=lambda: [add_link()])
        apply_button.grid(row=2, column=0, sticky="ew")

        def add_link():
            if os.path.exists('Source/Resources/link.txt'):
                try:
                    with open('Source/Resources/link.txt', 'r+b') as file:
                        loaded_data = pickle.load(file)
                except EOFError:
                    return {}
                if "entry" in loaded_data:
                    entry = loaded_data["entry"]
                    entry.append({'entry_link': link_entry.get(), 'entry_name': name_entry.get()})
                    data = {'entry': entry}
                else:
                    data = data = {'entry': [{'entry_link': link_entry.get(), 'entry_name': name_entry.get()}]}
            else:
                data = {'entry': [{'entry_link': link_entry.get(), 'entry_name': name_entry.get()}]}
            with open('Source/Resources/link.txt', 'wb') as file:
                pickle.dump(data, file)

            self.link_data = self.load_link()

    def new_instant_task(self):

        instant_task_window = tk.Toplevel(root)
        instant_task_window.title("New task")
        instant_task_window.minsize(550, 350)

        menubar = tk.Menu(instant_task_window)
        filemenu = tk.Menu(menubar, tearoff=0)
        # filemenu.add_command(label="Undo", command=input_text.undo, accelerator="Ctrl+Z")
        # filemenu.add_command(label="Redo", accelerator="Ctrl+Y")
        filemenu.add_command(label="Read from file", command=self.read_input, accelerator="Ctrl+O")
        filemenu.add_command(label="Close", command=instant_task_window.destroy)
        menubar.add_cascade(label="File", menu=filemenu)

        actionmenu = tk.Menu(menubar, tearoff=0)
        actionmenu.add_command(label="Send", underline=0,
                               command=lambda: self.handle_messenger(input_text.get("1.0", tk.END)),
                               accelerator="Ctrl+Enter")
        actionmenu.add_command(label="Add Link", command=self.add_link, accelerator="Control+L")
        menubar.add_cascade(label="Actions", menu=actionmenu)

        instant_task_window.config(menu=menubar)

        login_frame = ttk.LabelFrame(instant_task_window, text="Recipient Details")
        login_frame.grid(row=0, column=1, sticky="new")
        login_frame.grid_rowconfigure([0], weight=1, minsize=50)
        login_frame.grid_columnconfigure([0], weight=1, minsize=130)

        link_label = ttk.Label(login_frame, text="(Optional) Link: ")
        link_label.grid(row=0, column=0, sticky="w")
        tooltip.CreateToolTip(link_label, text=Texts.text.link_tooltip)
        link_entry = tkinterextension.LabelEntry(login_frame, label="100000178957952")
        link_entry.grid(row=0, column=1)

        if bool(self.data):
            link_entry.delete(0, tk.END)
            link_entry.insert("end", self.data["link"])

        def fetch_link(idx):
            link_entry.delete(0, tk.END)
            link_entry.insert("end", self.link_data["entry"][idx]["entry_link"])

        if "entry" in self.link_data:
            entry = self.link_data["entry"]
            nested_menu = tk.Menu(actionmenu)
            for index, link in enumerate(entry):
                nested_menu.add_command(label=link["entry_name"], command=partial(fetch_link, index))
            # nested_menu.add_command(label="See all", command=list_links) todo add see all link function
            actionmenu.add_cascade(label="Auto insert links", menu=nested_menu)

        input_frame = ttk.LabelFrame(instant_task_window, text="Text")
        input_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        input_frame.grid_rowconfigure([0], weight=1)
        input_frame.grid_columnconfigure([0], weight=1)

        input_label = ttk.Label(input_frame, text="Input")
        input_label.grid(row=0, column=0)
        tooltip.CreateToolTip(input_label, text=Texts.text.input_tooltip)
        input_text = tk.Text(input_frame, undo=True)
        input_text.insert("end", Texts.text.examplequote if not self.data or "text" not in self.data else self.data[
            "text"])
        input_text.grid(row=1, column=0)

        filemenu.add_command(label="Undo", command=input_text.edit_undo, accelerator="Ctrl+Z")
        filemenu.add_command(label="Redo", command=input_text.edit_redo, accelerator="Ctrl+Y")

        technical_frame = ttk.LabelFrame(instant_task_window, text="Options")
        technical_frame.grid(row=1, column=1, sticky="new")
        technical_frame.grid_rowconfigure([0, 1], weight=1)
        technical_frame.grid_columnconfigure([0, 1], weight=1)

        method_label = ttk.Label(master=technical_frame, text="Send option:")
        method_label.grid(row=0, column=0, sticky="w")
        send_method = ttk.Combobox(master=technical_frame, width=10, state="readonly",
                                   textvariable=self.method)
        send_method['values'] = ('Plain text', 'Caption')
        send_method.current(0 if not self.settings_data or "method" not in self.settings_data
                            else self.settings_data["method"])
        send_method.grid(row=0, column=1, sticky="w")

        iteration_label = ttk.Label(master=technical_frame, text="Iteration:")
        iteration_label.grid(row=1, column=0, sticky="w", pady=15)
        iteration_box = ttk.Spinbox(master=technical_frame, width=4, from_=1, to=100, wrap=True,
                                    textvariable=self.iteration_value)
        iteration_box.grid(row=1, column=1, sticky="w")

        instant_task_window.grid_rowconfigure(0, weight=1)
        instant_task_window.grid_columnconfigure(0, weight=1)

        # menu popup
        popup = tk.Menu(input_text, tearoff=0)
        popup.add_command(label="Add divider", command=self.add_divider, accelerator="Alt+D")
        popup.add_command(label="Clear", command=self.clear_input, accelerator="Ctrl+Q")
        popup.add_separator()

        apply_button = ttk.Button(master=instant_task_window, text="Send", command=lambda: [
            self.handle_messenger(input_text.get("1.0", tk.END))])
        apply_button.grid(row=2, column=0, sticky="ews")

    def new_schedule(self):
        schedule_window = tk.Toplevel(root)
        schedule_window.title("New schedule task")
        schedule_window.minsize(550, 350)

        menubar = tk.Menu(schedule_window)
        filemenu = tk.Menu(menubar, tearoff=0)
        # filemenu.add_command(label="Undo", command=input_text.undo, accelerator="Ctrl+Z")
        # filemenu.add_command(label="Redo", accelerator="Ctrl+Y")
        filemenu.add_command(label="Read from file", command=self.read_input, accelerator="Ctrl+O")
        filemenu.add_command(label="Close", command=schedule_window.destroy)
        menubar.add_cascade(label="File", menu=filemenu)

        actionmenu = tk.Menu(menubar, tearoff=0)
        actionmenu.add_command(label="Send", underline=0,
                               command=lambda: self.handle_messenger(input_text.get("1.0", tk.END)),
                               accelerator="Ctrl+Enter")
        actionmenu.add_command(label="Add Link", command=self.add_link, accelerator="Control+L")
        menubar.add_cascade(label="Actions", menu=actionmenu)

        schedule_window.config(menu=menubar)

        login_frame = ttk.LabelFrame(schedule_window, text="Recipient Details")
        login_frame.grid(row=0, column=1, sticky="new")
        login_frame.grid_rowconfigure([0], weight=1, minsize=50)
        login_frame.grid_columnconfigure([0], weight=1, minsize=130)

        link_label = ttk.Label(login_frame, text="(Optional) Link: ")
        link_label.grid(row=0, column=0, sticky="w")
        tooltip.CreateToolTip(link_label, text=Texts.text.link_tooltip)
        link_entry = tkinterextension.LabelEntry(login_frame, label="100000178957952")
        link_entry.grid(row=0, column=1)

        if bool(self.data):
            link_entry.delete(0, tk.END)
            link_entry.insert("end", self.data["link"])

        def fetch_link(idx):
            link_entry.delete(0, tk.END)
            link_entry.insert("end", self.link_data["entry"][idx]["entry_link"])

        if "entry" in self.link_data:
            entry = self.link_data["entry"]
            nested_menu = tk.Menu(actionmenu)
            for index, link in enumerate(entry):
                nested_menu.add_command(label=link["entry_name"], command=partial(fetch_link, index))
            # nested_menu.add_command(label="See all", command=list_links) todo add see all link function
            actionmenu.add_cascade(label="Auto insert links", menu=nested_menu)

        input_frame = ttk.LabelFrame(schedule_window, text="Text")
        input_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        input_frame.grid_rowconfigure([0], weight=1)
        input_frame.grid_columnconfigure([0], weight=1)

        input_label = ttk.Label(input_frame, text="Input")
        input_label.grid(row=0, column=0)
        tooltip.CreateToolTip(input_label, text=Texts.text.input_tooltip)
        input_text = tk.Text(input_frame, undo=True)
        input_text.insert("end",
                          Texts.text.examplequote if not self.data or "text" not in self.data else self.data[
                              "text"])
        input_text.grid(row=1, column=0)

        filemenu.add_command(label="Undo", command=input_text.edit_undo, accelerator="Ctrl+Z")
        filemenu.add_command(label="Redo", command=input_text.edit_redo, accelerator="Ctrl+Y")

        technical_frame = ttk.LabelFrame(schedule_window, text="Options")
        technical_frame.grid(row=1, column=1, sticky="new")
        technical_frame.grid_rowconfigure([0, 1], weight=1)
        technical_frame.grid_columnconfigure([0, 1], weight=1)

        method_label = ttk.Label(master=technical_frame, text="Send option:")
        method_label.grid(row=0, column=0, sticky="w")
        send_method = ttk.Combobox(master=technical_frame, width=10, state="readonly",
                                   textvariable=self.method)
        send_method['values'] = ('Plain text', 'Caption')
        send_method.current(0 if not self.settings_data or "method" not in self.settings_data
                            else self.settings_data["method"])
        send_method.grid(row=0, column=1, sticky="w")

        iteration_label = ttk.Label(master=technical_frame, text="Iteration:")
        iteration_label.grid(row=1, column=0, sticky="w", pady=15)
        iteration_box = ttk.Spinbox(master=technical_frame, width=4, from_=1, to=100, wrap=True,
                                    textvariable=self.iteration_value)
        iteration_box.grid(row=1, column=1, sticky="w")

        scheduler_label = ttk.Label(master=technical_frame, text="Schedule:")
        scheduler_label.grid(row=2, column=0, sticky="w")
        # todo check possible bug that occur when 00 is passed instead of 0
        scheduler_hour = ttk.Spinbox(master=technical_frame, width=5, from_=0, to=23, increment=1,
                                     textvariable=self.hour, wrap=True)
        scheduler_hour.grid(row=2, column=1, sticky="w", padx=0)
        scheduler_minute = ttk.Spinbox(master=technical_frame, width=5, from_=0, to=59, increment=15,
                                       textvariable=self.min, wrap=True)
        scheduler_minute.grid(row=2, column=1, sticky="w", padx=55)
        scheduler_hourlabel = ttk.Label(technical_frame, text="Hours")
        scheduler_hourlabel.grid(row=2, column=1, sticky="w", padx=110)

        schedule_window.grid_rowconfigure(0, weight=1)
        schedule_window.grid_columnconfigure(0, weight=1)

        # menu popup
        popup = tk.Menu(input_text, tearoff=0)
        popup.add_command(label="Add divider", command=self.add_divider, accelerator="Alt+D")
        popup.add_command(label="Clear", command=self.clear_input, accelerator="Ctrl+Q")
        popup.add_separator()

        apply_button = ttk.Button(master=schedule_window, text="Add schedule",
                                  command=lambda: [
                                      self.scheduler.add_schedule(link=link_entry.get(),
                                                                  text=input_text.get("1.0", tk.END),
                                                                  hour=scheduler_hour.get(),
                                                                  minute=scheduler_minute.get()),
                                      self.update_schedule()])
        apply_button.grid(row=2, column=0, sticky="ews")

    def update_schedule(self):

        def remover(idx):
            self.scheduler.remove_schedule(idx)
            self.update_schedule()

        for item in self.scheduled_frame.winfo_children():
            item.destroy()

        self.schedules = self.scheduler.load_schedules()

        for idx, schedule in enumerate(self.schedules):
            # ttk.Label(self.scheduled_frame, text=f'{schedule["ref_label"]}').grid(row=idx, column=0)
            ttk.Label(self.scheduled_frame, text=f'{schedule["hour"]}:{schedule["minute"]} hours').grid(row=idx,
                                                                                                        column=0)
            ttk.Button(self.scheduled_frame, text="Remove",
                       command=partial(remover, idx)) \
                .grid(row=idx, column=1, padx=25, pady=5, sticky="e")

    # todo start scheduler when main window starts
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

    # shows exit prompt when users press 'X' button
    def override_close(self):
        if self.minimize_radio.get() == 2:
            self.hide_window()
        elif self.minimize_radio.get() == 3:
            root.destroy()
        else:
            res = tk.messagebox.askyesnocancel('Close Window', 'Minimize window '
                                                               'instead of closing? This is essential for '
                                                               'scheduled tasks to happen. (Changable in Setings)')
            if res:
                self.hide_window()
                pass
            elif res is False:
                root.destroy()
                pass
            elif res is None:
                pass

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
        systray = SysTrayIcon("Source/Resources/Icon/picturexviewer.ico", "Cappribot", menu_options,
                              default_menu_index=0)
        systray.start()

    def show_window(self):
        root.deiconify()

    def handle_messenger(self, text="", idx=-1):
        # self.save_data()
        if idx != -1:
            if "email" not in self.data:  # todo prompt user to set credentials
                pass
            else:
                schedule = self.scheduler.load_schedules(idx)
                self.handler.handle_message(text, self.data["email"],
                                            self.data["password"],
                                            schedule["link"], schedule["method"], int(schedule["iteration"])
                                            , self.settings_data["headless"])
        else:
            if "email" not in self.data:  # todo prompt user to set credentials
                pass
            else:
                self.handler.handle_message(text, self.data["email"],
                                            self.data["password"],
                                            self.data["link"], self.method.get(), self.iteration_value.get()
                                            , self.settings_data["headless"])
            # self.handler.handle_message(self.input_text.get("1.0", tk.END), self.email_entry.get(),
            #                             self.password_entry.get(),
            #                             self.link_entry.get(), self.method.get(), self.iteration_value.get()
            #                             , self.headless.get())

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
        self.save_settings()

    def save_settings(self):
        data = {'save_cred': self.save_cred.get(),
                'headless': self.headless.get(),
                'minimize_radio': self.minimize_radio.get()
                }
        # 'method': self.send_method.current()}
        with open('Source/Resources/settings.txt', 'wb') as file:
            pickle.dump(data, file)

    def load_data(self):
        if os.path.exists('Source/Resources/save.txt'):
            try:
                with open('Source/Resources/save.txt', 'r+b') as file:
                    return pickle.load(file)
            except EOFError:
                return {}

    def load_link(self):
        if os.path.exists('Source/Resources/link.txt'):
            try:
                with open('Source/Resources/link.txt', 'r+b') as file:
                    return pickle.load(file)
            except EOFError:
                return {}

    def clear_creds(self):
        data = {'email': "example@email.com", 'link': "100000178957952", 'password': "12345678"
                #             'text': self.input_text.get("1.0", tk.END)
                }
        with open('Source/Resources/save.txt', 'wb') as file:
            pickle.dump(data, file)
        self.data = self.load_data()
    # def save_data(self):
    #     self.save_settings()
    #     # if self.save_cred.get() is False:
    #     #     data = {'email': False, 'link': False,
    #     #             'text': self.input_text.get("1.0", tk.END)
    #     #             }
    #     # else:
    #     #     data = {'email': self.email_entry.get(), 'link': self.link_entry.get(),
    #     #             'text': self.input_text.get("1.0", tk.END)
    #     #             }
    #     data = {'email': self.email_entry.get(), 'link': self.link_entry.get(),
    #             'text': self.input_text.get("1.0", tk.END)
    #             }
    #     with open('Source/Resources/save.txt', 'wb') as file:
    #         pickle.dump(data, file)


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
root.title("Cappribot v0.2.5a")
root.iconphoto(False, tk.PhotoImage(file='Source/Resources/Icon/gradient_less_saturated.png'))
root.resizable(False, False)
app = Application(master=root)
app.mainloop()
