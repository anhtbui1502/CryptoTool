#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
    Author: tungdd
    Date created: 19/11/2023
"""
import tkinter as tk


class BaseScreen(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

    def calculate_x_y_in_center_windows(self, x_input, y_input):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        return (screen_width - x_input) // 2, (screen_height - y_input) // 2