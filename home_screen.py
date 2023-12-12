#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
    Author: tungdd
    Date created: 15/11/2023
"""
import socket
import tkinter as tk
from tkinter import ttk
import bybit_api


from base_screen import BaseScreen


class HomeScreen(BaseScreen):
    WIDTH = 1430
    HEIGHT = 700

    def __init__(self, master):
        super().__init__(master)

        self.circle_check_online = None
        self.button_switch = None
        self.row_next = 0
        self.is_switch_on = False

        self.configure(bg='white')
        self.title("Home")

        self.canvas = tk.Canvas(self, width=30, height=30, bg="white", highlightthickness=0,
                                highlightbackground="white")
        self.canvas.grid(row=0, column=13)
        x, y = self.calculate_x_y_in_center_windows(self.WIDTH, self.HEIGHT)
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}+{x}+{y}")
        # self.geometry("%dx%d" % (self.WIDTH, self.HEIGHT))
        self.resizable(False, False) # Khong cho resize

        self._setup_style()
        self.check_connection_internet()
        self.create_label_and_entry_pairs()

        self.create_target()

        button_update_command = ttk.Button(self, text="Update command", width=22,
                                           command=lambda: print("Update Command"), style="Custom.TButton")
        button_update_command.grid(row=self.row_next, columnspan=2, column=4, padx=12, pady=6)

        self._set_row_next(self.row_next + 1)

        text_view = tk.Text(self, background="white", foreground="#000", font=('Arial', 12))
        text_view.grid(row=0, column=8, rowspan=9, columnspan=3, padx=10, pady=10)

        self.create_table_show_data()

        self.create_frame_logout()

        self.withdraw()
        self.protocol("WM_DELETE_WINDOW", self.master.quit_app)

    @classmethod
    def _setup_style(cls):
        treeview_style = ttk.Style()
        treeview_style.theme_use("clam")
        treeview_style.configure("Custom.Treeview", background="white")
        treeview_style.configure("Custom.Treeview.Heading", background="#e6e6ff", foreground="black")

        button_background_color = "#4ddbff"
        button_style = ttk.Style()
        button_style.configure("Custom.TButton", background=button_background_color, foreground="black")
        button_style.map(
            "Custom.TButton",
            background=[("pressed", button_background_color), ("active", button_background_color),
                        ("disabled", button_background_color)],
            foreground=[("pressed", "black"), ("active", "black"), ("disabled", "black")]
        )
        # button_style.configure("Custom.TButton", background="blue", relief=tk.FLAT)

        entry_style = ttk.Style()
        entry_style.configure("Custom.Entry", background="white", fieldbackground="white", bordercolor="gray")

    def create_frame_logout(self):

        button_logout = ttk.Button(self, text="Logout", command=lambda: self.master.process_logout(),
                                   style="Custom.TButton")
        button_logout.grid(row=0, column=11, padx=2, columnspan=2, pady=1)

        self.circle_check_online = self.canvas.create_oval(5, 5, 25, 25, fill="green")

        label_volume = ttk.Label(self, text="Volume:")
        label_volume.grid(row=1, column=11, padx=2, sticky=tk.W, pady=1)

        entry_volume = ttk.Entry(self, width=10)
        entry_volume.grid(row=1, column=12, pady=1)

        label_leverage = ttk.Label(self, text="Leverage:")
        label_leverage.grid(row=2, column=11, padx=2, sticky=tk.W, pady=1)
        # Tแบกo Combobox
        self.combo_leverage = ttk.Combobox(self, values=self._load_option_leverage_selected(), width=8, background="white",
                                           foreground="black")
        self.combo_leverage.grid(row=2, column=12, pady=1)

        label_isolated = tk.ttk.Label(self, text="Isolated:")
        label_isolated.grid(row=3, column=11, padx=2, sticky=tk.W, pady=1)

        self.toggle_switch_isolated()

        label_start_date = tk.ttk.Label(self, text="Start date:")
        label_start_date.grid(row=12, column=11, padx=2, sticky=tk.W, pady=1)

        entry_start_date = ttk.Entry(self, width=10)
        entry_start_date.grid(row=12, column=12, pady=1)

        label_end_date = tk.ttk.Label(self, text="End date:")
        label_end_date.grid(row=13, column=11, padx=2, sticky=tk.W, pady=1)
        entry_end_date = ttk.Entry(self, width=10)
        entry_end_date.grid(row=13, column=12, pady=1)

        button_update_date = tk.ttk.Button(self, text="Update Date", command=lambda: print("Update Date"),
                                           style="Custom.TButton")
        button_update_date.grid(row=14, column=11, columnspan=2, padx=2, pady=1)

        button_start = tk.ttk.Button(self, text="START", command=lambda: print("Button Start"), style="Custom.TButton")
        button_start.grid(row=15, column=11, columnspan=2, padx=2, pady=1)

        button_pause = tk.ttk.Button(self, text="PAUSE", command=lambda: print("Button Pause"), style="Custom.TButton")
        button_pause.grid(row=16, column=11, columnspan=2, padx=2, pady=1)

        button_stop_system = tk.ttk.Button(self, text="STOP SYSTEM", command=lambda: print("Button stop system"),
                                           style="Custom.TButton")
        button_stop_system.grid(row=17, column=11, columnspan=2, padx=2, pady=1)

        self.combo_leverage.bind("<<ComboboxSelected>>", self._on_leverage_selected)

    def _load_option_leverage_selected(self):
        return ["Option 1", "Option 2", "Option 3"]

    def _on_leverage_selected(self, event):
        selected_leverage = self.combo_leverage.get()

    @classmethod
    def is_connected_internet(cls):
        try:
            socket.create_connection(("www.google.com", 80), timeout=5)
            return True
        except OSError:
            return False

    def check_connection_internet(self):
        connected = self.is_connected_internet()
        if connected:
            self.canvas.itemconfig(self.circle_check_online, fill="green")
        else:
            self.canvas.itemconfig(self.circle_check_online, fill="red")
        self.after(5000, self.check_connection_internet)

    def action_toggle_isolated(self):
        if self.is_switch_on:
            self.button_switch.config(image=self.master.switch_off_image)
            self.is_switch_on = False

        else:
            self.button_switch.config(image=self.master.switch_on_image)
            self.is_switch_on = True

    def toggle_switch_isolated(self):
        self.button_switch = tk.Button(self,
                                       image=self.master.switch_off_image,
                                       bd=0,
                                       command=self.action_toggle_isolated,
                                       width=50, height=30
                                       )
        self.button_switch.grid(row=3, column=12, padx=1, sticky=tk.W, pady=6)

    def create_label_and_entry_pairs(self):
        label_one_texts = [
            ("Id:", ""),
            ("Command code:", ""),
            ("Type:", ""),
            ("Date:", ""),
            ("Price:", ""),
            ("Entry price:", ""),
            ("Status:", "")
        ]

        entries = []

        for i, (label_text, entry_text) in enumerate(label_one_texts):
            label = ttk.Label(self, text=label_text)
            label.grid(row=i, column=0, padx=10, sticky=tk.W, pady=1)
            entry = ttk.Entry(self, width=20)
            entry.grid(row=i, column=1, pady=1)
            entry.insert(0, entry_text)  # Set default text if needed
            entries.append(entry)

        return entries

    def create_target(self):
        label_targets = [
            ("Target 1:", "", 2),
            ("Target 2:", "", 2),
            ("Target 3:", "", 2),
            ("Target 4:", "", 2),
            ("Target 5:", "", 2),
            ("Stop loss:", "", 1),
            ("Volume:", "", 1)
        ]
        for i, (label_text, entry_text, number) in enumerate(label_targets):
            label = ttk.Label(self, text=label_text)
            label.grid(row=i, column=3, padx=2, sticky=tk.W, pady=1)
            if number == 2:
                entry_one = ttk.Entry(self, width=5)
                entry_one.grid(row=i, column=4, pady=1)
                entry_one.insert(0, entry_text)
                entry_two = ttk.Entry(self, width=5)
                entry_two.grid(row=i, column=5, pady=1)
                entry_two.insert(0, entry_text)  # Set default text if needed
            else:
                entry_one = ttk.Entry(self, width=13)
                entry_one.grid(row=i, column=4, pady=1, columnspan=2)
                entry_one.insert(0, entry_text)

        self._set_row_next(len(label_targets))

        return

    @classmethod
    def _convert_text_to_column(cls, text):
        return text.lower().replace(" ", "_")

    def create_table_show_data(self):

        frame_show_table = tk.Frame(self)
        frame_show_table.grid(row=self.row_next + 2, column=0, rowspan=20, columnspan=10, padx=10, pady=10, sticky=tk.W)

        vertical_scroll = tk.Scrollbar(frame_show_table)
        vertical_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        horizontal_scroll = tk.Scrollbar(frame_show_table, orient='horizontal')
        horizontal_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        # Treeview widget
        table_info = ttk.Treeview(frame_show_table, yscrollcommand=vertical_scroll.set,
                                  xscrollcommand=horizontal_scroll.set, show="headings", style="Custom.Treeview",
                                  height=10)

        # Set command for scrolls
        vertical_scroll.config(command=table_info.yview)
        horizontal_scroll.config(command=table_info.xview)

        mapping_headers_width = {
            "Symbol": 90,
            "Type": 90,
            "Date": 90,
            "Leverage": 90,
            "EntryPrice": 90,
            "MarkPrice": 90,
            "Volume": 90,
            "Pnl": 90,
            "Target 1": 90,
            "Target 2": 90,
            "Target 3": 90,
            "Target 4": 90,
            "Target 5": 90,
            "Stop loss": 90
        }

        table_info["columns"] = [self._convert_text_to_column(key) for key in mapping_headers_width.keys()]

        for header, width in mapping_headers_width.items():
            index = self._convert_text_to_column(header)
            table_info.heading(index, text=header, anchor=tk.CENTER)
            table_info.column(index, anchor=tk.CENTER, width=width)

        # # Sample data
        # data = [
        #     ('1', 'Ninja', '101', 'Oklahoma', 'Moore'),
        #     ('2', 'Ranger', '102', 'Wisconsin', 'Green Bay'),
        #     ('2', 'Ranger', '102', 'Wisconsin', 'Green Bay'),
        #     ('2', 'Ranger', '102', 'Wisconsin', 'Green Bay'),
        #     ('2', 'Ranger', '102', 'Wisconsin', 'Green Bay'),
        #     ('2', 'Ranger', '102', 'Wisconsin', 'Green Bay'),
        #     ('2', 'Ranger', '102', 'Wisconsin', 'Green Bay'),
        #     ('2', 'Ranger', '102', 'Wisconsin', 'Green Bay'),
        #     ('2', 'Ranger', '102', 'Wisconsin', 'Green Bay'),
        #     ('2', 'Ranger', '102', 'Wisconsin', 'Green Bay'),
        #     ('2', 'Ranger', '102', 'Wisconsin', 'Green Bay'),
        #     ('2', 'Ranger', '102', 'Wisconsin', 'Green Bay', '1.2'),
        # ]
        table_info.pack(fill='both', expand=True)
        self.fill_table(table_info,frame_show_table)
        # frame_show_table.mainloop()

    def fill_table(self, table_info, frame_show_table):
        data = bybit_api.get_current_position()
        for item in data.values.tolist():
            table_info.insert(parent='', index='end', values=item)
		# Đoạn code này dùng reload table
        # frame_show_table.after(600000, self.fill_table(table_info, frame_show_table))


    def _set_row_next(self, row):
        self.row_next = row + 1
