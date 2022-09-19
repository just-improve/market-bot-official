import tkinter as tk
from tkinter import ttk
from tkinter import messagebox



class View(tk.Tk):
    PAD = 10

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title('Market Bot')
        self._make_main_frame()
        self._make_entry()
        self._make_button()


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
        self.gap_reverse_long_entry.insert(1,1.0001)
        self.gap_reverse_long_entry.pack(fill='x')

        self.gap_reverse_short_entry = ttk.Entry(self.main_frm, justify='right')
        self.gap_reverse_short_entry.insert(0, 0.9999)
        self.gap_reverse_short_entry.pack(fill='x')

        self.gap_profit_long_entry = ttk.Entry(self.main_frm, justify='right')
        self.gap_profit_long_entry.insert(0,1.001)
        self.gap_profit_long_entry.pack(fill='x')

        self.gap_profit_short_entry = ttk.Entry(self.main_frm, justify='right')
        self.gap_profit_short_entry.insert(0,0.999)
        self.gap_profit_short_entry.pack(fill='x')

        self.refresh_time_entry = ttk.Entry(self.main_frm, justify='right')
        self.refresh_time_entry.insert(0,2)
        self.refresh_time_entry.pack(fill='x')

        self.market_fee_entry = ttk.Entry(self.main_frm, justify='right')
        self.market_fee_entry.insert(0, 0.00064505)
        self.market_fee_entry.pack(fill='x')

        self.running_result_var = tk.StringVar()
        self.label_running_result = ttk.Label(self.main_frm, textvariable=self.running_result_var)
        self.label_running_result.pack()

        self.total_result_var = tk.StringVar()
        self.label_total_result = ttk.Label(self.main_frm, textvariable=self.total_result_var)
        self.label_total_result.pack()

        self.list_of_trades_var = tk.StringVar()
        self.label_list_of_trades = ttk.Label(self.main_frm, textvariable=self.list_of_trades_var)
        self.label_list_of_trades.pack()

        self.prices_will_var = tk.StringVar()
        self.label_prices_will = ttk.Label(self.main_frm, textvariable=self.prices_will_var)
        self.label_prices_will.pack()


    def _make_button(self):  # single underscore is private method

        btn = ttk.Button(self.main_frm, text='start', command=self.controller.start_bot)
        btn.pack(fill='x')

        btn_stop = ttk.Button(self.main_frm, text='stop', command=self.store_trades_and_finish)
        btn_stop.pack(fill='x')

        btn2 = ttk.Button(self.main_frm, text='Show trade list', command=self.show_trades)
        btn2.pack(fill='x')

    def store_trades_and_finish(self):
        #self.controller.on_button_click_stop_program_and_save()
        #self.controller.model.end_time =
        self.controller.on_button_click_stop_program_and_save_txt()



    def show_trades(self):
        list_of_tr = self.controller.list_as_string_in_new_line(self.controller.model.list_of_trades)
        #list_of_tr = ""
        #for x in self.controller.model.list_of_trades:
            #list_of_tr=list_of_tr+str(x)+"\n"
        messagebox.showinfo("showinfo", list_of_tr)



