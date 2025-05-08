import tkinter as tk
from tkinter import ttk, StringVar
from tkinter.ttk import Combobox
import requests
import json

LARGEFONT = ("Verdana", 35)

user = {
    'name': "",
    'email': "",
    'uname': "",
    'token': ""
}

class SubscriberClient(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Subscriber App")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginPage, RegisterPage, MainPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def validate_login(self, uname, password):
        print("Validating Login")
        request_data = {'action': 'login', 'uname': uname, 'pass': password}
        try:
            response = requests.post('http://localhost:25678', json=request_data, timeout=10)
            response_data = json.loads(response.content.decode())
            print(response_data['message'])
            if response_data['error'] is False:
                user.update({
                    'name': response_data['name'],
                    'email': response_data['email'],
                    'uname': response_data['uname'],
                    'token': response_data['token']
                })
                self.show_frame(MainPage)
                self.frames[MainPage].write_uname(user['name'], user['token'])
            else:
                self.frames[LoginPage].write_error(response_data['message'])
        except Exception as e:
            print("Login error:", e)
            self.frames[LoginPage].write_error("something went wrong!!, Please try after some time")

    def register_req(self, name, uname, passwd, email):
        print("Register user")
        request_data = {'action': 'register', 'uname': uname, 'pass': passwd, 'name': name, 'email': email}
        try:
            response = requests.post('http://localhost:25678', json=request_data, timeout=10)
            response_data = json.loads(response.content.decode())
            print(response_data['message'])
            if response_data['error'] is False:
                self.show_frame(LoginPage)
                self.frames[LoginPage].write_error(response_data['message'])
            else:
                self.frames[RegisterPage].write_error(response_data['message'])
        except Exception as e:
            print("Register error:", e)
            self.frames[RegisterPage].write_error("something went wrong!!, Please try after some time")

    def subscribe_topic(self, topic):
        print(f"Subscribing to topic: {topic}")
        try:
            request_data = {'action': 'subscribe', 'topic': topic, 'uname': user['uname']}
            response = requests.post('http://localhost:25678', json=request_data, timeout=10)
            response_data = json.loads(response.content.decode())
            if not response_data['error']:
                self.frames[MainPage].write_uname(response_data['message'], user['token'])
            else:
                self.frames[MainPage].write_uname(response_data['message'], user['token'])
        except Exception as e:
            print("Subscribe error:", e)
            self.frames[MainPage].write_uname("Subscription failed. Try again later.", user['token'])


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        ttk.Label(self, text="Login/Register", font=LARGEFONT).grid(row=0, column=4)
        ttk.Label(self, text="Username/Email").grid(row=1, column=4)
        uname_e = ttk.Entry(self)
        uname_e.grid(row=2, column=4, padx=10, pady=10)
        ttk.Label(self, text="Password").grid(row=3, column=4, padx=10, pady=10)
        passw_e = ttk.Entry(self, show="*")
        passw_e.grid(row=4, column=4, padx=10, pady=10)
        ttk.Button(self, text="Log In", command=lambda: controller.validate_login(uname_e.get(), passw_e.get())).grid(row=1, column=1, padx=10, pady=10)
        ttk.Button(self, text="Register", command=lambda: controller.show_frame(RegisterPage)).grid(row=2, column=1, padx=10, pady=10)
        ttk.Label(self, text="New here? click on Register").grid(row=5, column=4, padx=10, pady=10)
        self.tooltip_l = ttk.Label(self)
        self.tooltip_l.grid(row=6, column=4, padx=10, pady=10)

    def write_error(self, msg):
        self.tooltip_l.config(text=msg, foreground="red")


class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        ttk.Label(self, text="Registration Form", font=LARGEFONT).grid(row=0, columnspan=2, sticky="e")
        ttk.Label(self, text="Name").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        name_r = ttk.Entry(self)
        name_r.grid(row=1, column=1, padx=10, pady=10)
        ttk.Label(self, text="Username").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        uname_r = ttk.Entry(self)
        uname_r.grid(row=2, column=1, padx=10, pady=10)
        ttk.Label(self, text="Password").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        pass_r = ttk.Entry(self, show="*")
        pass_r.grid(row=3, column=1, padx=10, pady=10)
        ttk.Label(self, text="Email").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        email_r = ttk.Entry(self, show="*")
        email_r.grid(row=4, column=1, padx=10, pady=10)
        ttk.Button(self, text="Back", command=lambda: controller.show_frame(LoginPage)).grid(row=5, column=0, padx=10, pady=10)
        ttk.Button(self, text="Register", command=lambda: controller.register_req(name_r.get(), uname_r.get(), pass_r.get(), email_r.get())).grid(row=5, column=1, padx=10, pady=10)
        self.tooltip_l = ttk.Label(self)
        self.tooltip_l.grid(row=6, column=0, padx=10, pady=10)

    def write_error(self, msg):
        self.tooltip_l.config(text=msg, foreground="red")


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        ttk.Label(self, text="Main Page", font=LARGEFONT).grid(row=0, columnspan=1)
        ttk.Button(self, text="LogOut", command=lambda: controller.show_frame(LoginPage)).grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self, text="Choose Topic").grid(row=2, column=0, padx=10, pady=10)
        self.selected_topic = StringVar()
        self.topic_dropdown = Combobox(self, textvariable=self.selected_topic)
        self.topic_dropdown['values'] = ['World', 'US', 'Politics', 'Economy', 'Business', 'Tech', 'Markets', 'Sports']
        self.topic_dropdown.grid(row=2, column=1, padx=10, pady=10)

        ttk.Button(self, text="Subscribe", command=lambda: controller.subscribe_topic(self.selected_topic.get())).grid(row=3, column=1, padx=10, pady=10)

        self.tooltip_l = ttk.Label(self)
        self.tooltip_l.grid(row=6, column=0, padx=10, pady=10)

    def write_uname(self, name, token):
        self.tooltip_l.config(text=name + "\nToken: " + token, foreground="red")


# Driver Code
if __name__ == '__main__':
    app = SubscriberClient()
    app.mainloop()
