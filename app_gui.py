""""
Software Design Final Project: Trail Blazer

app_gui.py wraps up all the functions sofar created in an interactive GUI for the user.
"""

from tkinter import *
import intersections
import overpy

class TrailBlazerGUI:
    def __init__(self, master):
        self.master = master
        self.bg = "#90EE90"
        self.fg = "#654321"
        self.e_page = "empty"
        master.title("Trail Blazer")
        master.geometry("1920x1080")
        master.configure(bg=self.bg)
        master.bind("<Escape>", self.close)

        self.start = Frame(master, height=1080, width=1920, bg=self.bg)
        self.start.pack()
        self.start.focus_set()
        self.start.bind("<Return>", self.login_page)
        self.greet = Label(self.start, text="Welcome to our Route Suggestion Web App!", font=("sans serif", 50),
                            fg=self.fg, bg=self.bg, pady=10)
        self.greet.pack()
        self.intro = Message(self.start, text="We are writing software to help generate and visualize new routes for runners, walkers, and bikers. \nWe are creating this for our Software Design final project.",
                            font=("sans serif", 20), width=1900, justify=CENTER, fg=self.fg, bg=self.bg, pady=10)
        self.intro.pack()


        self.buttons1 = Frame(self.start, width=500, bg=self.bg)
        self.buttons1.pack()
        self.proceed = Button(self.buttons1, text="Proceed", bg="#64e764", fg="#654321", pady=5,
                                activebackground="#bcf5bc", activeforeground="#8b5d2e", command=self.login_page)
        self.proceed.grid(row=0, column=0)
        self.cancel = Button(self.buttons1, text="Cancel", bg="#64e764", fg="#654321", pady=5,
                                    activebackground="#bcf5bc", activeforeground="#8b5d2e", command=master.quit)
        self.cancel.grid(row=0, column=1)

        self.logo = PhotoImage(file="images/trail_blazer_logo.gif")
        self.logo_disp = Label(self.start, image=self.logo, fg=self.fg, bg=self.bg)
        self.logo_disp.pack(side=BOTTOM)

    def login_page(self, event=None):
        if self.e_page!="empty":
            self.e_page.pack_forget()
            self.e_page.destroy()
        else:
            self.start.pack_forget()
            self.start.destroy()
        self.l_page = Frame(self.master, height=1080, width=1920, bg=self.bg)
        self.l_page.pack()
        self.l_page.focus_set()
        self.l_page.bind("<Return>", self.valid_login)
        self.l_page.bind("<Escape>", self.close)


        self.request = Label(self.l_page, text="Please log in to continue.", font=("sans serif", 20),
                            fg=self.fg, bg=self.bg, pady=20)
        self.request.pack()


        self.login = Frame(self.l_page, width=1000, bg=self.bg)
        self.login.pack()
        self.login.bind("<Return>", self.valid_login)
        self.first = Label(self.login, text="First Name = ", font=("sans serif", 15), anchor=W, bg=self.bg,
                            fg=self.fg, pady=10)
        self.first.grid(row=0, sticky=E)
        self.first_in = Entry(self.login, font=("sans serif", 15), exportselection=0, cursor="xterm")
        self.first_in.bind("<Return>", self.valid_login)
        self.first_in.grid(row=0, column=1, columnspan=3)
        self.last = Label(self.login, text="Last Name = ", font=("sans serif", 15), anchor=W, bg=self.bg,
                            fg=self.fg, pady=10)
        self.last.grid(row=1, sticky=E)
        self.last_in = Entry(self.login, font=("sans serif", 15), exportselection=0, cursor="xterm")
        self.last_in.bind("<Return>", self.valid_login)
        self.last_in.grid(row=1, column=1, columnspan=3)
        self.user = Label(self.login, text="Username = ", font=("sans serif", 15), anchor=W, bg=self.bg,
                            fg=self.fg, pady=10)
        self.user.grid(row=2, sticky=E)
        self.user_in = Entry(self.login, font=("sans serif", 15), exportselection=0, cursor="xterm")
        self.user_in.bind("<Return>", self.valid_login)
        self.user_in.grid(row=2, column=1, columnspan=3)
        self.pss = Label(self.login, text="Password = ", font=("sans serif", 15), anchor=W, bg=self.bg,
                            fg=self.fg, pady=10)
        self.pss.grid(row=3, sticky=E)
        self.pss_in = Entry(self.login, font=("sans serif", 15), exportselection=0, cursor="xterm", show="*")
        self.pss_in.bind("<Return>", self.valid_login)
        self.pss_in.grid(row=3, column=1, columnspan=3)


        self.buttons2 = Frame(self.l_page, width=500, bg=self.bg)
        self.buttons2.pack()
        self.submit = Button(self.buttons2, text="Submit", bg="#64e764", fg="#654321", pady=5,
                            activebackground="#bcf5bc", activeforeground="#8b5d2e", command=self.valid_login)
        self.submit.bind("<Return>", self.valid_login)
        self.submit.grid(row=0, column=0)
        self.cancel = Button(self.buttons2, text="Cancel", bg="#64e764", fg="#654321", pady=5,
                            activebackground="#bcf5bc", activeforeground="#8b5d2e", command=self.master.quit)
        self.cancel.bind("<Return>", self.valid_login)
        self.cancel.grid(row=0, column=1)

    def home_page(self, event=None):
        first_name = self.first_in.get()
        last_name = self.last_in.get()
        self.l_page.pack_forget()
        self.l_page.destroy()
        self.h_page = Frame(self.master, height=1080, width=1920, bg=self.bg)
        self.h_page.pack()
        self.h_page.focus_set()
        self.h_page.bind("<Return>", self.find_route)
        self.h_page.bind("<Escape>", self.close)


        self.hello = Label(self.h_page, text="Hello! Welcome to your profile page!", font=("sans serif", 50),
                            bg=self.bg, fg=self.fg, pady=20)
        self.hello.pack()


        self.weather_init = Frame(self.h_page, width=1000, bg=self.bg)
        self.weather_init.pack()
        self.weather_init.bind("<Return>", self.get_forecast)
        self.location = Label(self.weather_init, text="Current Location = ", font=("sans serif", 15), anchor=W, bg=self.bg,
                            fg=self.fg, pady=10)
        self.location.grid(row=0, sticky=E)
        self.location_in = Entry(self.weather_init, font=("sans serif", 15), exportselection=0, cursor="xterm")
        self.location_in.bind("<Return>", self.get_forecast)
        self.location_in.grid(row=0, column=1)


        self.buttons5 = Frame(self.h_page, width=500, bg=self.bg)
        self.buttons5.pack()
        self.buttons5.bind("<Return>", self.get_forecast)
        self.weatherby = Button(self.buttons5, text="Find Weather", bg="#64e764", fg="#654321",
                            activebackground="#bcf5bc", activeforeground="#8b5d2e", pady=5, command=self.get_forecast)
        self.weatherby.grid(row=0, column=0)


        self.name_is = Label(self.h_page, text="Where would you like to go, %s %s?" % (first_name, last_name),
                            font=("sans serif", 15), fg=self.fg, bg=self.bg, pady=10)
        self.name_is.pack()


        self.profile = Frame(self.h_page, width=1000, bg=self.bg)
        self.profile.pack()
        self.profile.bind("<Return>", self.find_route)
        self.loc = Label(self.profile, text="Starting Location:", font=("sans serif", 15), anchor=W, bg=self.bg,
                            fg=self.fg, pady=10)
        self.loc.grid(row=0, sticky=E)
        self.lat = Label(self.profile, text="Latitiude = ", font=("sans serif", 15), anchor=W, bg=self.bg,
                            fg=self.fg, pady=10)
        self.lat.grid(row=1, column=0)
        self.lat_in = Entry(self.profile, font=("sans serif", 15), exportselection=0, cursor="xterm")
        self.lat_in.bind("<Return>", self.find_route)
        self.lat_in.insert(0,"42.292922")
        if self.profile.focus_get() == self.lat_in:
            self.lat_in.delete()
        self.lat_in.grid(row=1, column=1)
        self.lng = Label(self.profile, text="Longitude = ", font=("sans serif", 15), anchor=W, bg=self.bg,
                            fg=self.fg, pady=10)
        self.lng.grid(row=1, column=2)
        self.lng_in = Entry(self.profile, font=("sans serif", 15), exportselection=0, cursor="xterm")
        self.lng_in.bind("<Return>", self.find_route)
        self.lng_in.insert(0,"-71.263073")
        if self.profile.focus_get() == self.lat_in:
            self.lat_in.delete()
        self.lng_in.grid(row=1, column=3)
        self.dist = Label(self.profile, text="Distance(km) = ", font=("sans serif", 15), anchor=W, bg=self.bg,
                            fg=self.fg, pady=10)
        self.dist.grid(row=2, sticky=E)
        self.dist_in = Entry(self.profile, font=("sans serif", 15), exportselection=0, cursor="xterm")
        self.dist_in.bind("<Return>", self.find_route)
        self.dist_in.grid(row=2, column=1)
        self.dist_max = Label(self.profile, text="Maximum distance = 2", font=("sans serif", 10), anchor=W, bg=self.bg,
                            fg=self.fg, pady=10, padx=10)
        self.dist_max.grid(row=2, column=2, sticky=E)


        self.buttons3 = Frame(self.h_page, width=500, bg=self.bg)
        self.buttons3.pack()
        self.enter = Button(self.buttons3, text="Find Route", bg="#64e764", fg="#654321",
                            activebackground="#bcf5bc", activeforeground="#8b5d2e", pady=5, command=self.find_route)
        self.enter.grid(row=0, column=0)
        self.cancel = Button(self.buttons3, text="Cancel", bg="#64e764", fg="#654321",
                            activebackground="#bcf5bc", activeforeground="#8b5d2e",pady=5, command=self.master.quit)
        self.cancel.grid(row=0, column=1)

    def error(self, event=None):
        self.l_page.pack_forget()
        self.l_page.destroy()
        self.e_page = Frame(self.master, height=1080, width=1920, bg=self.bg)
        self.e_page.pack()
        self.e_page.focus_set()
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

    def valid_login(self,event=None):
        firstname = self.first_in.get()
        lastname = self.last_in.get()
        username = self.user_in.get()
        password = self.pss_in.get()
        if not firstname and not lastname and not username and not password:
            return self.error()
        else:
            return self.home_page()

    def get_forecast(self, event=None):
        from weather import Weather, Unit
        self.weather = Weather(unit=Unit.FAHRENHEIT)
        self.local = self.weather.lookup_by_location(self.location_in.get())
        self.condition = self.local.condition
        self.forecasts = self.local.forecast
        self.forecast = self.forecasts[1]


        self.location.destroy()
        self.location_in.destroy()
        self.buttons5.destroy()


        self.weather_1 = Label(self.weather_init, text="Today's weather will be %s and %s F" % (self.condition.text,self.condition.temp),
                                    font=("sans serif", 17), justify=CENTER, fg=self.fg, bg=self.bg)
        self.weather_1.pack()
        self.weather_2 = Label(self.weather_init, text="with a high of %s F and a low of %s F." % (self.forecast.high, self.forecast.low),
                                font=("sans serif", 15), justify=CENTER, fg=self.fg, bg=self.bg)
        self.weather_2.pack()
        self.weather_3 = Label(self.weather_init, text="According to Yahoo weather on %s." % (self.condition.date),font=("sans serif", 10),
                                justify=CENTER, fg=self.fg, bg=self.bg, pady=5)
        self.weather_3.pack()

    def find_route(self, event=None):
        api = overpy.Overpass()
        lat = float(self.lat_in.get())
        lng = float(self.lng_in.get())
        radius = 0.01
        distance = float(self.dist_in.get())
        print(lat,lng,distance)
        intersections.graph_it(api,lat,lng,radius,distance)

    def close(self, event=None):
        self.master.quit()

root = Tk()
app_gui = TrailBlazerGUI(root)
root.mainloop()
