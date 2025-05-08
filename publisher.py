# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 12:08:05 2025

@author: vvkgp
"""

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import requests
import json
import socket
import sqlite3

host = 'localhost'
LARGEFONT = ("Verdana", 35)

user = {
    'name': "",
    'email': "",
    'uname': "",
    'token': ""
}

# retrieve the subs for a Topic given the topic name
def get_subs():
    with sqlite3.connect('data/topics.db') as conn:
        cursor = conn.execute('SELECT name FROM topics')
        result = cursor.fetchall()
        return result

# retrieve the broker information
def broker_info(topic):
    with sqlite3.connect('data/brokers.db') as conn:
        cursor = conn.execute('SELECT port FROM brokers WHERE topic=?', (topic,))
        result = cursor.fetchone()
        return result

def all_brokers_info():
    with sqlite3.connect('data/brokers.db') as conn:
        cursor = conn.execute('SELECT * FROM brokers')
        result = cursor.fetchall()
        return result

topic_list = list(get_subs())
for i in range(len(topic_list)):
    topic_list[i] = topic_list[i][0]

class PublisherClient(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
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
            if not response_data['error']:
                user.update({
                    'name': response_data['name'],
                    'email': response_data['email'],
                    'uname': response_data['uname'],
                    'token': response_data['token']
                })
                self.show_frame(MainPage)
                self.frames[MainPage].write_uname(user['name'])
            else:
                self.frames[LoginPage].write_error(response_data['message'])
        except:
            self.frames[LoginPage].write_error("something went wrong!!, Please try after some time")

    def register_req(self, name, uname, passwd, email):
        print("Register user")
        request_data = {'action': 'register', 'uname': uname, 'pass': passwd, 'name': name, 'email': email}
        try:
            response = requests.post('http://localhost:25678', json=request_data, timeout=10)
            response_data = json.loads(response.content.decode())
            print(response_data['message'])
            if not response_data['error']:
                self.show_frame(LoginPage)
                self.frames[LoginPage].write_error(response_data['message'])
            else:
                self.frames[RegisterPage].write_error(response_data['message'])
        except:
            self.frames[RegisterPage].write_error("something went wrong!!, Please try after some time")

    def publish_req(self, content, topic, title):
        print(all_brokers_info())
        print(topic)
        b_port = broker_info(topic)

        if b_port is None:
            self.frames[MainPage].notifyevent_m("Topic not assigned to a broker.")
            return

        b_port = int(b_port[0])
        print(b_port)

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, b_port))

            data = {
                'content': content,
                'topic': topic,
                'title': title,
                'uname': user['uname']
            }
            json_data = json.dumps(data)

            sock.send(json_data.encode())
            sock.close()

            self.frames[MainPage].notifyevent_m("Message published successfully.")
        except Exception as e:
            print("Publish error:", e)
            self.frames[MainPage].notifyevent_m("Please try after some time.")

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
        self.search_box_var = tk.StringVar()
        self.tooltip_l = ttk.Label(self, text="Main Page", font=LARGEFONT)
        self.tooltip_l.pack(side="top")

        self.search_box = ttk.Entry(self, font=("Verdana", 12), textvariable=self.search_box_var)
        self.search_box.pack(side="top")

        self.results_box = tk.Listbox(self, yscrollcommand=True, height=2, selectmode=tk.SINGLE)
        self.results_box.pack(expand=0)
        self.results_box.delete(0, tk.END)

        tk.Label(self, text="Title", font=("Verdana", 15)).pack(side="top")
        self.title_m = tk.Entry(self, font=("Verdana", 12), xscrollcommand=True, width=50)
        self.title_m.pack(side="top")

        self.text_m = scrolledtext.ScrolledText(self)
        self.text_m.pack()

        ttk.Button(self, text="LogOut", command=lambda: controller.show_frame(LoginPage)).pack(side="right")
        ttk.Button(self, text="Publish", command=lambda: controller.publish_req(self.text_m.get("1.0", 'end-1c'), self.results_box.get(self.results_box.curselection()), self.title_m.get())).pack(side="right")

        self.notify_m = ttk.Label(self, font=("Verdana", 15))
        self.notify_m.pack(side="bottom")

        self.search_box_var.trace('w', self.update_search_results)

    def update_search_results(self, *args):
        search_str = self.search_box_var.get()
        matches = [item for item in topic_list if search_str.lower() in item.lower()]
        self.results_box.delete(0, tk.END)
        for match in matches:
            self.results_box.insert(tk.END, match)

    def write_uname(self, name):
        self.tooltip_l.config(text="Welcome " + name, foreground="red")

    def notifyevent_m(self, msg):
        self.notify_m.config(text=msg, foreground="red")

if __name__ == '__main__':
    app = PublisherClient()
    app.mainloop()
