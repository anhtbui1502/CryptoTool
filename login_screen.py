#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
    Author: tungdd
    Date created: 15/11/2023
"""
import tkinter as tk
from tkinter import ttk, messagebox

from base_screen import BaseScreen
import bybit_api


class LoginScreen(BaseScreen):
    WIDTH = 350
    HEIGHT = 150

    def __init__(self, master):
        super().__init__(master)
        self.title("Login")

        self.configure(bg='white')

        x, y = self.calculate_x_y_in_center_windows(self.WIDTH, self.HEIGHT)
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}+{x}+{y}")
        self.resizable(False, False)

        label_username = ttk.Label(self, text="Username:")
        label_username.grid(row=4, column=2, padx=20, pady=(30, 1))

        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(row=4, column=3, pady=(30, 1))

        label_password = ttk.Label(self, text="Password:")
        label_password.grid(row=5, column=2, padx=20, pady=1)

        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=5, column=3, pady=1)

        login_button = ttk.Button(self, text="Sign up", command=self.on_sign_up)
        login_button.grid(row=8, column=3, columnspan=2, pady=5)

        self.bind('<Return>', lambda event: self.enter_login(event))

        self.protocol("WM_DELETE_WINDOW", self.master.quit_app)

    def validate_credentials(self, entered_username, entered_password):
        username_default = "admin"
        password_default = "admin"

        if entered_username == username_default and entered_password == password_default:
            bybit_api.get_current_position()
            self.master.show_home_screen()
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Username or password incorrect!")

    def on_sign_up(self):
        entered_username = self.username_entry.get()
        entered_password = self.password_entry.get()

        if not entered_username or not entered_password:
            messagebox.showerror("Error", "Please enter username and password!")
        else:
            self.validate_credentials(entered_username, entered_password)

    def enter_login(self, event):
        entered_username = self.username_entry.get()
        entered_password = self.password_entry.get()

        if not entered_username or not entered_password:
            messagebox.showerror("Error", "Please enter username and password!")
        else:
            self.validate_credentials(entered_username, entered_password)

