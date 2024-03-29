import tkinter as tk
from tkinter import ttk


class View(tk.Tk):
    PAD = 10
    str10 = "hello"

    def __init__(self, controller):
        super().__init__()

        self.title('Market Bot')

        self.controller = controller

        self._make_main_frame()

        self._make_entry()
        self._make_button()
        self._make_button_with_argument()


    def main(self):
        self.mainloop()

    def _make_main_frame(self):
        self.main_frm = ttk.Frame(self)
        self.main_frm.pack(padx=self.PAD, pady=self.PAD)

    def _make_entry(self):  # single underscore is private method
        self.market_name_entry = ttk.Entry(self.main_frm, justify='right')
        self.market_name_entry.insert(1, "CEL-PERP")
        self.market_name_entry.pack(fill='x')

        self.gap_reverse_long_entry = ttk.Entry(self.main_frm, justify='right')
        self.gap_reverse_long_entry.insert(1,1.01)
        self.gap_reverse_long_entry.pack(fill='x')

        self.gap_reverse_short_entry = ttk.Entry(self.main_frm, justify='right')
        self.gap_reverse_short_entry.insert(0, 0.99)
        self.gap_reverse_short_entry.pack(fill='x')

        self.gap_profit_long_entry = ttk.Entry(self.main_frm, justify='right')
        self.gap_profit_long_entry.insert(0,1.05)
        self.gap_profit_long_entry.pack(fill='x')

        self.gap_profit_short_entry = ttk.Entry(self.main_frm, justify='right')
        self.gap_profit_short_entry.insert(0,0.95)
        self.gap_profit_short_entry.pack(fill='x')

        self.refresh_time_entry = ttk.Entry(self.main_frm, justify='right')
        self.refresh_time_entry.insert(0,2)
        self.refresh_time_entry.pack(fill='x')

        self.market_fee_entry = ttk.Entry(self.main_frm, justify='right')
        self.market_fee_entry.insert(0, 0.00064505)
        self.market_fee_entry.pack(fill='x')



    def _make_button(self):  # single underscore is private method

        btn = ttk.Button(self.main_frm, text='start', command=self.controller.on_button_click)
        btn.pack(fill='x')

    def _make_button_with_argument(self):  # single underscore is private method
        btn = ttk.Button(self.main_frm, text='stop', command=lambda gap_reverse=self.gap_reverse_long_entry: self.controller.on_button_click_with_argument(gap_reverse))
        btn.pack(fill='x')

