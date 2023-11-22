from datetime import *
import tkinter as tk
from tkinter import *


class Message:
    def __init__(self, message="None", ip="None", sender="Anonymous"):

        if message == "None":
            self.message = input("Please enter your message: ")
        else:
            self.message = message

        self.IP = ip
        self.message_sender = sender
        self.time_stamp = str(datetime.now())[:-10]

    def print_time(self):
        print(self.time_stamp)


class ChatLog:
    def __init__(self):
        self.message_list = []

        # Tkinter implementations
        self.main_window = tk.Tk()
        self.main_window.geometry("600x400")

        self.chat_frame_scroll_bar = tk.Scrollbar(self.main_window)
        self.chat_frame = tk.Text(self.main_window, state=DISABLED)
        self.chat_frame_scroll_bar.config(orient="vertical", command=self.chat_frame.yview)

        self.entry = tk.Entry(self.main_window, bg='grey')
        self.send_msg_button = tk.Button(self.main_window, bg='orange', text="send message", command=self.create_message)

    def create_chat_window(self):
        self.chat_frame_scroll_bar.pack(side=RIGHT, fill=Y)
        self.send_msg_button.pack(side=BOTTOM)
        self.entry.pack(side=BOTTOM)
        self.chat_frame.pack(side=BOTTOM)

        self.chat_frame_scroll_bar.config(command=self.chat_frame.yview)

        self.main_window.bind("<Return>", lambda event: self.create_message())
        self.main_window.mainloop()

    def add_message(self, message_obj):
        self.message_list.append(message_obj)
        self.chat_frame.config(state=NORMAL)
        self.chat_frame.insert(END, f"{message_obj.time_stamp}<{message_obj.message_sender}>: {message_obj.message}\n")
        self.chat_frame.config(state=DISABLED)
        self.chat_frame.see(END)

    def print_log(self):
        for msg in self.message_list:
            print(msg.message)

    def create_message(self):
        new_message_string = self.entry.get()
        self.entry.delete(0, END)
        if new_message_string.isspace() or new_message_string == "":
            return
        print(new_message_string)
        new_message_object = Message(message=new_message_string)
        self.add_message(new_message_object)


""" -----------------------------------------------------Notes----------------------------------------------------------





"""