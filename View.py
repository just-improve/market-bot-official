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

        self.minVolatility1h_lab = ttk.Label(self.main_frm, text="MinVolatility1h")
        self.minVolatility1h_lab.pack(fill='x')

        self.min_vol_1h_entry = ttk.Entry(self.main_frm, justify='right')
        self.min_vol_1h_entry.insert(1, 0.02)
        self.min_vol_1h_entry.pack(fill='x')

        self.gap_reverse_long_entry_lab = ttk.Label(self.main_frm, text="gap_reverse_long_entry")
        self.gap_reverse_long_entry_lab.pack(fill='x')

        self.gap_reverse_long_entry = ttk.Entry(self.main_frm, justify='right')
        self.gap_reverse_long_entry.insert(1,1.03)
        self.gap_reverse_long_entry.pack(fill='x')

        self.gap_reverse_short_entry_lab = ttk.Label(self.main_frm, text="gap_reverse_short_entry")
        self.gap_reverse_short_entry_lab.pack(fill='x')

        self.gap_reverse_short_entry = ttk.Entry(self.main_frm, justify='right')
        self.gap_reverse_short_entry.insert(0, 0.97)
        self.gap_reverse_short_entry.pack(fill='x')

        self.gap_profit_long_entry_lab = ttk.Label(self.main_frm, text="gap_profit_long_entry")
        self.gap_profit_long_entry_lab.pack(fill='x')

        self.gap_profit_long_entry = ttk.Entry(self.main_frm, justify='right')
        self.gap_profit_long_entry.insert(0,1.005)
        self.gap_profit_long_entry.pack(fill='x')

        self.gap_profit_short_entry_lab = ttk.Label(self.main_frm, text="gap_profit_short_entry")
        self.gap_profit_short_entry_lab.pack(fill='x')

        self.gap_profit_short_entry = ttk.Entry(self.main_frm, justify='right')
        self.gap_profit_short_entry.insert(0,0.995)
        self.gap_profit_short_entry.pack(fill='x')

        self.refresh_time_lab = ttk.Label(self.main_frm, text="refresh time")
        self.refresh_time_lab.pack(fill='x')

        self.refresh_time_entry = ttk.Entry(self.main_frm, justify='right')
        self.refresh_time_entry.insert(0,2)
        self.refresh_time_entry.pack(fill='x')

        self.market_fee_lab = ttk.Label(self.main_frm, text="market fee")
        self.market_fee_lab.pack(fill='x')

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

        self.status_info_var = tk.StringVar()
        self.status_info_lab = ttk.Label(self.main_frm, textvariable=self.status_info_var)
        self.status_info_lab.pack()


    def _make_button(self):  # single underscore is private method

        btn = ttk.Button(self.main_frm, text='start', command=self.controller.start_bot)
        btn.pack(fill='x')

        btn_stop = ttk.Button(self.main_frm, text='stop', command=self.stop_main_while)
        btn_stop.pack(fill='x')

        btn2 = ttk.Button(self.main_frm, text='Show trade list', command=self.show_trades)
        btn2.pack(fill='x')

        btn3 = ttk.Button(self.main_frm, text='Show playing markets', command=self.show_playing_markets)
        btn3.pack(fill='x')

        btn4 = ttk.Button(self.main_frm, text='Show fields of playing markets', command=self.show_fields_of_playning_market)
        btn4.pack(fill='x')

    def stop_main_while(self):
        self.controller.on_button_click_while_bot_stop()

    def show_trades(self):
        list_of_tr = self.controller.list_as_string_in_new_line(self.controller.model.list_of_all_trades)
        messagebox.showinfo("showinfo", list_of_tr)

    def show_playing_markets(self):
        list_of_tr =  str(len(self.controller.model.list_of_playing_markets_model)) + '\n'
        #len_of_list_obj = str(len(self.controller.model.list_of_playing_markets_model)) + '\n'
        for x in self.controller.model.list_of_playing_markets_model:
            list_of_tr=list_of_tr+x.market_name+'\n'

        #list_of_tr = self.controller.list_as_string_in_new_line(self.controller.model.list_of_playing_markets_model)
        messagebox.showinfo("showinfo", list_of_tr)

    def show_fields_of_playning_market(self):
        list_as_str = ""
        for x in self.controller.model.list_of_playing_markets_model:
            print("")
            list_of_fileds = []
            list_of_fileds.append(str(x.market_name))
            list_of_fileds.append(str(x.change1h) + " change1h")
            list_of_fileds.append(str(len(self.controller.model.list_of_playing_markets_model)) + " len os playing obj ")
            list_of_fileds.append(str(x.won_or_lost) + " won_or_lost")
            list_of_fileds.append(str(x.is_playing) + " is playing")
            list_of_fileds.append(str(x.status) + " status")
            list_of_fileds.append(str(x.bid) + " " + str(x.ask) + " bidy aski")
            list_of_fileds.append(str(x.entry_price) + " entry_price")
            list_of_fileds.append(str(x.closed_price) + " closed_price")
            list_of_fileds.append(str(x.stoploss_price_will) + " stoploss_price_will")
            list_of_fileds.append(str(x.long_profit_price_will) + " long_profit_price_will")
            list_of_fileds.append(str(x.short_profit_price_will) + " short_profit_price_will")

            for x in list_of_fileds:
                list_as_str = list_as_str + x + '\n'
            #print(list_as_str)

        messagebox.showinfo("showinfo", list_as_str)



