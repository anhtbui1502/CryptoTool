#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
    Author: tungdd
    Date created: 19/11/2023
"""
import sys
import tkinter as tk

from home_screen import HomeScreen
from login_screen import LoginScreen


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.switch_on_image = tk.PhotoImage(file="image/switch_on.png")
        self.switch_off_image = tk.PhotoImage(file="image/switch_off.png")
        self.title("Ứng dụng đăng nhập")
        self.configure(bg='white')
        self.withdraw()
        self.login_screen = LoginScreen(self)
        self.home_screen = HomeScreen(self)

    def show_home_screen(self):
        self.login_screen.withdraw()
        self.home_screen.deiconify()

    def process_logout(self):
        self.home_screen.withdraw()
        self.login_screen.deiconify()

    def quit_app(self):
        self.destroy()
        sys.exit(0)
