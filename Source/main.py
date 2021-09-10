import ctypes
import random
import os
import tkinter as tk
import tkinter.ttk as ttk
import pickle
from messengerhandler import Handler as Handler


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.data = self.load_data()
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
        self.email_entry.insert("end", 'veixhen@hotmail.com' if not self.data else self.data["email"])
        self.email_entry.grid(row=0, column=1)

        self.password_label = ttk.Label(self.login_frame, text="Password:")
        self.password_label.grid(row=1, column=0)
        self.password_entry = ttk.Entry(self.login_frame)
        self.password_entry.grid(row=1, column=1)

        self.link_label = ttk.Label(self.login_frame, text="Link:")
        self.link_label.grid(row=2, column=0)
        self.link_entry = ttk.Entry(self.login_frame)
        self.link_entry.insert("end", "100000178957922" if not self.data else self.data["link"])
        self.link_entry.grid(row=2, column=1)

        self.input_frame = ttk.LabelFrame(text="Text")
        self.input_frame.grid(row=1, column=0, sticky="nsew")
        self.input_frame.grid_rowconfigure([0], weight=1)
        self.input_frame.grid_columnconfigure([0], weight=1)

        self.input_label = ttk.Label(self.input_frame, text="Input")
        self.input_label.grid(row=0, column=0)
        self.input_text = tk.Text(self.input_frame)
        self.input_text.insert("end", """
Example (notice the symbols)
_______________________________
#thecatthrifts #thrifting #preloved #secondhand #thriftmalaysia #onlinethriftstore #thriftstore #stylewithus #thriftwithusthursdays #thriftstorefinds #eighthdrop #rainbow #tops #shorts #lowrise #unique #vintage #retro #valuebuy #slowfashionisthewaytogo #sustainablefashion #sustainability #supportsmallbusiness #smallbusiness #staysafestayhome #thecatthriftsavailable
&thecatthriftsavailabletop &thecatthriftsavailablebottom &thecatthriftsavailabledress &thecatthriftsavailablejacket

$$
Red long sleeve shirt

-
fits XS-S
7/10
RM13 (includes postage)

Shoulder 14
Sleeves 20
Bust 13.5
Length 19
&1
$$
Red skirt with safety pants

-
fits M-small L
8/10 
RM13 (includes postage)

Waist 15
Hips 19.5
Length 13.5
&2""" if not self.data else self.data["text"])
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
        data = {'email': self.email_entry.get(), 'link': self.link_entry.get(),
                'text': self.input_text.get("1.0", tk.END)}
        with open('Source/Resources/save.txt', 'wb') as file:
            pickle.dump(data, file)


root = tk.Tk()
# ttk.Style().configure("TButton", padding=6, relief="flat", foreground="#E8E8E8", background="#292929")
root.geometry("1000x563")
root.title("Cappribot v0.1.0a")
root.iconphoto(False, tk.PhotoImage(file='Source/Resources/Icon/gradient_less_saturated.png'))
root.resizable(False, False)
app = Application(master=root)
app.mainloop()
