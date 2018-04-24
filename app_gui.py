"""
Code for the creation and running of the GUI for Trail Blazer.
"""

from tkinter import *
from AnimatedGif import *

class TrailBlazerGUI:
    def __init__(self, master):
        self.master = master
        self.bg = "#90EE90"
        self.fg = "#654321"
        self.e_page = "empty"
        master.title("Trail Blazer")
        master.geometry("1920x1080")
        master.configure(bg=self.bg)
        master.bind("<Return>", self.login_page)
        master.bind("<Escape>", self.close)


        self.greet = Label(master, text="Welcome to our Route Suggestion Web App!", font=("sans serif", 50),
                            fg=self.fg, bg=self.bg, pady=10)
        self.greet.pack()
        self.intro = Message(master, text="We are writing software to help generate and visualize new routes for runners, walkers, and bikers. \nWe are creating this for our Software Design final project.",
                            font=("sans serif", 20), width=1900, justify=CENTER, fg=self.fg, bg=self.bg, pady=10)
        self.intro.pack()


        self.buttons1 = Frame(master, width=500, bg=self.bg)
        self.buttons1.pack()
        self.proceed = Button(self.buttons1, text="Proceed", bg="#64e764", fg="#654321", pady=5,
                                activebackground="#bcf5bc", activeforeground="#8b5d2e", command=self.login_page)
        self.proceed.grid(row=0, column=0)
        self.cancel = Button(self.buttons1, text="Cancel", bg="#64e764", fg="#654321", pady=5,
                                    activebackground="#bcf5bc", activeforeground="#8b5d2e", command=master.quit)
        self.cancel.grid(row=0, column=1)

        self.gif = AnimatedGif(master, 'images/oregonTrail.gif', 0.5)
        self.gif.config(background=self.bg)
        self.gif.pack(side=BOTTOM)
        self.gif.start()

    def login_page(self, event=None):
        self.gif.stop()
        self.l_page = Toplevel(bg=self.bg)
        self.l_page.geometry("1920x1080")
        if self.e_page!="empty":
            self.e_page.withdraw()
        self.master.withdraw()
        self.l_page.bind("<Return>", self.valid_login)
        self.l_page.bind("<Escape>", self.close)


        self.request = Label(self.l_page, text="Please log in to continue.", font=("sans serif", 20),
                            fg=self.fg, bg=self.bg, pady=20)
        self.request.pack()


        self.login = Frame(self.l_page, width=1000, bg=self.bg)
        self.login.pack()
        self.first = Label(self.login, text="First Name = ", font=("sans serif", 15), anchor=W, bg=self.bg,
                            fg=self.fg, pady=10)
        self.first.grid(row=0, sticky=E)
        self.first_in = Entry(self.login, font=("sans serif", 15), exportselection=0, cursor="xterm")
        self.first_in.grid(row=0, column=1, columnspan=3)
        self.last = Label(self.login, text="Last Name = ", font=("sans serif", 15), anchor=W, bg=self.bg,
                            fg=self.fg, pady=10)
        self.last.grid(row=1, sticky=E)
        self.last_in = Entry(self.login, font=("sans serif", 15), exportselection=0, cursor="xterm")
        self.last_in.grid(row=1, column=1, columnspan=3)
        self.user = Label(self.login, text="Username = ", font=("sans serif", 15), anchor=W, bg=self.bg,
                            fg=self.fg, pady=10)
        self.user.grid(row=2, sticky=E)
        self.user_in = Entry(self.login, font=("sans serif", 15), exportselection=0, cursor="xterm")
        self.user_in.grid(row=2, column=1, columnspan=3)
        self.pss = Label(self.login, text="Password = ", font=("sans serif", 15), anchor=W, bg=self.bg,
                            fg=self.fg, pady=10)
        self.pss.grid(row=3, sticky=E)
        self.pss_in = Entry(self.login, font=("sans serif", 15), exportselection=0, cursor="xterm", show="*")
        self.pss_in.grid(row=3, column=1, columnspan=3)


        self.buttons2 = Frame(self.l_page, width=500, bg=self.bg)
        self.buttons2.pack()
        self.submit = Button(self.buttons2, text="Submit", bg="#64e764", fg="#654321", pady=5,
                            activebackground="#bcf5bc", activeforeground="#8b5d2e", command=self.valid_login)
        self.submit.grid(row=0, column=0)
        self.cancel = Button(self.buttons2, text="Cancel", bg="#64e764", fg="#654321", pady=5,
                            activebackground="#bcf5bc", activeforeground="#8b5d2e", command=self.master.quit)
        self.cancel.grid(row=0, column=1)

    def home_page(self, event=None):
        self.l_page.withdraw()
        self.h_page = Toplevel(bg=self.bg)
        self.h_page.geometry("1920x1080")
        self.h_page.bind("<Return>", self.find_route)
        self.h_page.bind("<Escape>", self.close)

        self.hello = Label(self.h_page, text="Hello! Welcome to your profile page!", font=("sans serif", 50),
                            bg=self.bg, fg=self.fg, pady=20)
        self.hello.pack()

        self.weather_init = Frame(self.h_page, width=1000, bg=self.bg)
        self.weather_init.pack()

        self.name_is = Label(self.h_page, text="Where would you like to go, %s %s?" % (self.first_in.get(), self.last_in.get()),
                            font=("sans serif", 15), fg=self.fg, bg=self.bg, pady=10)
        self.name_is.pack()

        self.profile = Frame(self.h_page, width=1000, bg=self.bg)
        self.profile.pack()
        self.loc = Label(self.profile, text="Starting Location = ", font=("sans serif", 15), anchor=W, bg=self.bg,
                            fg=self.fg, pady=10)
        self.loc.grid(row=0, sticky=E)
        self.loc_in = Entry(self.profile, font=("sans serif", 15), exportselection=0, cursor="xterm")
        self.loc_in.grid(row=0, column=1)
        self.dist = Label(self.profile, text="Distance(km) = ", font=("sans serif", 15), anchor=W, bg=self.bg,
                            fg=self.fg, pady=10)
        self.dist.grid(row=1, sticky=E)
        self.dist_in = Entry(self.profile, font=("sans serif", 15), exportselection=0, cursor="xterm")
        self.dist_in.grid(row=1, column=1)


        self.buttons3 = Frame(self.h_page, width=500, bg=self.bg)
        self.buttons3.pack()
        self.enter = Button(self.buttons3, text="Find Route", bg="#64e764", fg="#654321",
                            activebackground="#bcf5bc", activeforeground="#8b5d2e", pady=5, command=self.find_route)
        self.enter.grid(row=0, column=0)
        self.cancel = Button(self.buttons3, text="Cancel", bg="#64e764", fg="#654321",
                            activebackground="#bcf5bc", activeforeground="#8b5d2e",pady=5, command=self.master.quit)
        self.cancel.grid(row=0, column=1)

    def error(self, event=None):
        self.e_page = Toplevel(bg=self.bg)
        self.e_page.geometry("1920x1080")
        self.l_page.withdraw()
        self.e_page.bind("<Return>", self.login_page)
        self.e_page.bind("<Escape>", self.close)

        self.err_title = Label(self.e_page, text="Error: Missing Information", font=("sans serif", 50),
                                bg=self.bg, fg=self.fg, pady=10)
        self.err_title.pack()
        self.err_mss = Message(self.e_page, text="Your submission was missing some data. All fields are rquired.\nPlease return to fill out all fields.",
                            font=("sans serif", 20), width=1900, justify=CENTER, fg=self.fg, bg=self.bg, pady=10)
        self.err_mss.pack()


        self.buttons4 = Frame(self.e_page, width=500, bg=self.bg)
        self.buttons4.pack()
        self.ret = Button(self.buttons4, text="Return", bg="#64e764", fg="#654321", pady=5,
                            activebackground="#bcf5bc", activeforeground="#8b5d2e", command=self.login_page)
        self.ret.grid(row=0, column=0)
        self.cancel = Button(self.buttons4, text="Cancel", bg="#64e764", fg="#654321", pady=5,
                            activebackground="#bcf5bc", activeforeground="#8b5d2e", command=self.master.quit)
        self.cancel.grid(row=0, column=1)

    def valid_login(self, event=None):
        firstname = self.first_in.get()
        lastname = self.last_in.get()
        username = self.user_in.get()
        password = self.pss_in.get()
        if not firstname and not lastname and not username and not password:
            return self.error()
        else:
            return self.home_page()

    def find_route(self, event=None):
        pass

    def close(self, event=None):
        self.master.quit()

root = Tk()
app_gui = TrailBlazerGUI(root)
root.mainloop()