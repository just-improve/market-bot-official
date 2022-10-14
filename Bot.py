import time

from View import View
from pool_executor import thread_pool_executor, submit_to_pool_executor
from test import Test
import datetime
import tkinter as tk
from tkinter import *

from Ftx_methods import FtxClientWJ


class Bot_class:

    def __init__(self, market: str, gap_long, gap_short, gap_profit_long, gap_profit_short, refresh_time, fee: float , view, controller):
        self.controller = controller
        self.view = view
        self.dt = datetime


    def __del__(self):
        print("")
    def get_future_with_1h_vol(self):
        obj_ftx_methods = FtxClientWJ()  #Na pewno to jest potrzebne
        min_change_1h = 0.02
        all_futures = obj_ftx_methods.get_all_futures()
        perp_list_of_dict = Test.get_list_of_perp_dict(all_futures)
        list_of_dict_vol_1h_rest = Test.get_list_dict_volatility_1h_restricted(perp_list_of_dict, min_change_1h)
        highest_vol_dict = Test.get_highest_vol_dict(list_of_dict_vol_1h_rest)
        print("mariusz")
        print(highest_vol_dict['name'])
        return highest_vol_dict['name']

    @submit_to_pool_executor(thread_pool_executor)
    def start_bot2(self):
        obj_ftx_methods = FtxClientWJ()  #Na pewno to jest potrzebne
        mainWhile = True
        isVolatility = False
        long_status = False
        short_status = False
        long_profit_status = False
        short_profit_status = False

        while mainWhile:

            while isVolatility is False:
                self.get_future_with_1h_vol()
                time.sleep(120)

                #warunek sprawdzający czy jest zmienność jeśli jest zmienność to wtedy zmienia boola i przechodzi do initialize
                if 3 > 2:
                    print("Pawel")
                    isVolatility = False


            while isVolatility is True:
                while long_status:
                    #za każdym trejdem sprawdzać czy jest inny coin o większej zmienności i wtedy zmienić na innego coina - to ma sens
                    #ponieważ i tak płącimy prowizję za zamknięcie pozycji więc lepiej jest jak gramy coina bardziej zmiennego
                    #raczej tego coina bym wolał zmieniać tylko w przypadku ewentualnych przegranych trejdów
                    przekręceniesie_stopLoss=""
                    if przekręceniesie_stopLoss:
                        #sprawdzenie_zmienności coinów - jeśli nasz spadł na dalekie miejsce to wtedy gramy ten najbardziej zmienny
                        # jeśli inny
                        pass

                while short_status:
                    pass
                while long_profit_status:
                    pass
                while short_profit_status:
                    pass
            while isVolatility is False:
                # zapisanie danych do pliku csv
                pass


    @submit_to_pool_executor(thread_pool_executor)
    def start_bot(self):
        obj_ftx_methods = FtxClientWJ()
        first_price = obj_ftx_methods.get_future(self.controller.model.market_name)["bid"]
        self.controller.model.start_time = self.dt.datetime.now().replace(microsecond=0)
        prc_init_long = 1.0001  # jedna dziesiąta procenta zmiany ceny
        prc_init_short = 0.9999  # jedna dziesiąta procenta zmiany ceny    zmiana ceny o 20 $ około
        long_price_sps_will = 0
        short_price_lps_will = 0
        self.controller.model.long_price_will = first_price * self.controller.model.gap_reverse_long_init
        self.controller.model.short_price_will = first_price * self.controller.model.gap_reverse_short_init
        self.view.prices_will_var.set("Prices will "+str(self.controller.model.long_price_will) + " " + str(self.controller.model.short_price_will))
        long_profit_price_will = 0
        short_profit_price_will = 0
        main_while = False
        long_status = False
        short_status = False
        long_profit_status = False
        short_profit_status = False
        initialize_while = True
        #stop_bot_by_stop_button = False

        # pętla inicjalizująca w celu wszedł w jakąś pozycję
        while initialize_while:
            print("\n petla inicializująca   ")
            time.sleep(self.controller.model.refresh_time)
            self.controller.model.last_bid_price  = obj_ftx_methods.get_future(self.controller.model.market_name)["bid"]
            self.controller.model.last_ask_price = obj_ftx_methods.get_future(self.controller.model.market_name)["ask"]
            self.view.running_result_var.set(str(self.controller.model.running_result) + " running result init")
            self.view.total_result_var.set(str(self.controller.model.total_result) + " total result")

            #trejdd initialize long
            if self.controller.model.last_ask_price >= self.controller.model.long_price_will:
                initialize_while = False
                long_status = True
                main_while = True

                self.controller.model.previous_entry_price = self.controller.model.last_entry_price
                self.controller.model.last_entry_price=self.controller.model.last_ask_price
                self.controller.model.last_long_or_short = "long"

                self.controller.model.short_price_will = self.controller.model.last_ask_price * self.controller.model.gap_reverse_short
                self.controller.model.long_price_will = 0
                self.view.prices_will_var.set("Prices will " + str(self.controller.model.long_price_will) + " " + str(self.controller.model.short_price_will))

                long_profit_price_will = self.controller.model.last_ask_price * self.controller.model.gap_profit_long
                short_profit_price_will = 0

                date_time_current = self.dt.datetime.now().replace(microsecond=0)
                trade = ["long", self.controller.model.last_ask_price, str(date_time_current)]

                self.controller.model.last_closed_result_no_fee = Test.calculate_last_result_2(self.controller.model.previous_entry_price,self.controller.model.last_entry_price,self.controller.model.last_long_or_short)
                self.controller.model.total_trades_result = self.controller.model.total_trades_result + self.controller.model.last_closed_result_no_fee
                self.controller.model.list_of_trades_results.append(self.controller.model.last_closed_result_no_fee)
                self.controller.model.list_of_trades_total_running_results.append(self.controller.model.total_trades_result)
                self.controller.model.sum_of_fees = self.controller.model.sum_of_fees + self.controller.model.fee
                self.controller.model.total_result=-self.controller.model.sum_of_fees + self.controller.model.total_trades_result

                trade.append(self.controller.model.list_of_settings_as_str)
                trade.append(self.controller.model.total_result)
                trade.append(self.controller.model.final_session_result)
                self.controller.model.list_of_trades.append(trade)
                self.controller.model.last_trade = trade

            # trejdd initialize short
            elif self.controller.model.last_bid_price <= self.controller.model.short_price_will:
                initialize_while = False
                short_status = True
                main_while = True

                self.controller.model.previous_entry_price = self.controller.model.last_entry_price
                self.controller.model.last_entry_price=self.controller.model.last_bid_price
                self.controller.model.last_long_or_short = "short"

                self.controller.model.long_price_will = self.controller.model.last_bid_price * self.controller.model.gap_reverse_long
                self.controller.model.short_price_will = 0
                self.view.prices_will_var.set("Prices will "+str(self.controller.model.long_price_will) + " " + str(self.controller.model.short_price_will))

                short_profit_price_will = self.controller.model.last_bid_price * self.controller.model.gap_profit_short
                long_profit_price_will = 0

                date_time_current = self.dt.datetime.now().replace(microsecond=0)
                trade = ["short", self.controller.model.last_bid_price, str(date_time_current)]

                self.controller.model.last_closed_result_no_fee = Test.calculate_last_result_2(self.controller.model.previous_entry_price, self.controller.model.last_entry_price,                    self.controller.model.last_long_or_short)
                self.controller.model.total_trades_result = self.controller.model.total_trades_result + self.controller.model.last_closed_result_no_fee
                self.controller.model.list_of_trades_results.append(self.controller.model.last_closed_result_no_fee)
                self.controller.model.list_of_trades_total_running_results.append(self.controller.model.total_trades_result)
                self.controller.model.sum_of_fees = self.controller.model.sum_of_fees + self.controller.model.fee
                self.controller.model.total_result = -self.controller.model.sum_of_fees + self.controller.model.total_trades_result

                trade.append(self.controller.model.list_of_settings_as_str)
                trade.append(self.controller.model.total_result)
                trade.append(self.controller.model.final_session_result)
                self.controller.model.list_of_trades.append(trade)
                self.controller.model.last_trade = trade

        while main_while and self.controller.model.stop_bot_by_stop_button is False:
            time.sleep(0.1)

            while long_status and self.controller.model.stop_bot_by_stop_button is False:
                print("\nLong status and now pause 2sec")
                time.sleep(self.controller.model.refresh_time)
                dict_future = obj_ftx_methods.get_future(self.controller.model.market_name)
                self.controller.model.last_ask_price = dict_future["ask"]
                self.controller.model.last_bid_price = dict_future["bid"]
                self.controller.model.running_result = Test.calculate_running_result(self.controller.model.last_entry_price,self.controller.model.last_bid_price,self.controller.model.fee,self.controller.model.last_long_or_short)
                self.view.running_result_var.set(str(self.controller.model.running_result) + " running result in long")
                total_res = float("{:.5f}".format(self.controller.model.total_result))
                self.view.total_result_var.set(str(total_res) + " total result")
                self.view.list_of_trades_var.set("bid ask "+ str(self.controller.model.last_bid_price)+ " "+ str(self.controller.model.last_ask_price))

                # trejdd short
                if self.controller.model.last_bid_price <= self.controller.model.short_price_will:
                    long_status = False
                    short_status = True

                    self.controller.model.previous_entry_price = self.controller.model.last_entry_price
                    self.controller.model.last_entry_price = self.controller.model.last_bid_price
                    self.controller.model.last_long_or_short = "short"

                    self.controller.model.long_price_will = self.controller.model.last_ask_price * self.controller.model.gap_reverse_long
                    self.controller.model.short_price_will = 0
                    self.view.prices_will_var.set("Prices will "+str(self.controller.model.long_price_will) + " " + str(self.controller.model.short_price_will))

                    short_profit_price_will = self.controller.model.last_bid_price * self.controller.model.gap_profit_short
                    long_profit_price_will = 0

                    date_time_current = self.dt.datetime.now().replace(microsecond=0)
                    trade = ["short", self.controller.model.last_bid_price, str(date_time_current)]

                    self.controller.model.last_closed_result_no_fee = Test.calculate_last_result_2(self.controller.model.previous_entry_price, self.controller.model.last_entry_price,self.controller.model.last_long_or_short)
                    self.controller.model.total_trades_result = self.controller.model.total_trades_result + self.controller.model.last_closed_result_no_fee
                    self.controller.model.list_of_trades_results.append(self.controller.model.last_closed_result_no_fee)
                    self.controller.model.list_of_trades_total_running_results.append(self.controller.model.total_trades_result)
                    self.controller.model.sum_of_fees = self.controller.model.sum_of_fees + self.controller.model.fee*2
                    self.controller.model.total_result = -self.controller.model.sum_of_fees + self.controller.model.total_trades_result

                    trade.append(self.controller.model.last_closed_result_no_fee)
                    trade.append(self.controller.model.total_result)
                    trade.append(self.controller.model.final_session_result)
                    self.controller.model.list_of_trades.append(trade)
                    self.controller.model.last_trade = trade

                elif self.controller.model.last_ask_price >= long_profit_price_will:
                    long_profit_status = True
                    long_status = False
                    print("trejd long_profit_status z long_status")
                    long_profit_price_will = 0
                    self.controller.model.long_price_will = 0
                    self.controller.model.short_price_will = self.controller.model.last_ask_price * self.controller.model.gap_profit_short
                    self.view.prices_will_var.set("Prices will "+
                                                  str(self.controller.model.long_price_will) + " " + str(self.controller.model.short_price_will))
                    short_price_lps_will = self.controller.model.last_ask_price * self.controller.model.gap_profit_short
                    print("W LongStatus do LongProfitStatus ")

            while short_status and self.controller.model.stop_bot_by_stop_button is False:
                print("\nShort status and now pause 2sec")
                time.sleep(self.controller.model.refresh_time)
                dict_future = obj_ftx_methods.get_future(self.controller.model.market_name)
                self.controller.model.last_ask_price = dict_future["ask"]
                self.controller.model.last_bid_price = dict_future["bid"]
                self.controller.model.running_result = Test.calculate_running_result(self.controller.model.last_entry_price,self.controller.model.last_ask_price,self.controller.model.fee,self.controller.model.last_long_or_short)
                self.view.running_result_var.set(str(self.controller.model.running_result) + " running result in short")
                total_res = float("{:.5f}".format(self.controller.model.total_result))
                self.view.total_result_var.set(str(total_res) + " total result")
                self.view.list_of_trades_var.set("bid ask "+ str(self.controller.model.last_bid_price)+ " "+ str(self.controller.model.last_ask_price))

                # trejdd long
                if self.controller.model.last_ask_price > self.controller.model.long_price_will:
                    long_status = True
                    short_status = False

                    self.controller.model.previous_entry_price = self.controller.model.last_entry_price
                    self.controller.model.last_entry_price = self.controller.model.last_ask_price
                    self.controller.model.last_long_or_short = "long"

                    self.controller.model.short_price_will = self.controller.model.last_bid_price * self.controller.model.gap_profit_short
                    self.view.prices_will_var.set("Prices will "+ str(self.controller.model.long_price_will) + " " + str(self.controller.model.short_price_will))

                    long_profit_price_will = self.controller.model.last_ask_price * self.controller.model.gap_profit_short
                    short_profit_price_will = 0

                    date_time_current = self.dt.datetime.now().replace(microsecond=0)
                    trade = ["long", self.controller.model.last_ask_price, str(date_time_current)]

                    self.controller.model.last_closed_result_no_fee = Test.calculate_last_result_2(self.controller.model.previous_entry_price, self.controller.model.last_entry_price,self.controller.model.last_long_or_short)
                    self.controller.model.total_trades_result = self.controller.model.total_trades_result + self.controller.model.last_closed_result_no_fee
                    self.controller.model.list_of_trades_results.append(self.controller.model.last_closed_result_no_fee)
                    self.controller.model.list_of_trades_total_running_results.append(self.controller.model.total_trades_result)
                    self.controller.model.sum_of_fees = self.controller.model.sum_of_fees + self.controller.model.fee*2
                    self.controller.model.total_result = -self.controller.model.sum_of_fees + self.controller.model.total_trades_result

                    trade.append(self.controller.model.last_closed_result_no_fee)
                    trade.append(self.controller.model.total_result)
                    trade.append(self.controller.model.final_session_result)

                    self.controller.model.list_of_trades.append(trade)
                    self.controller.model.last_trade = trade

                elif self.controller.model.last_bid_price < short_profit_price_will:
                    short_profit_status = True
                    short_status = False
                    print("trejd short_profit_status z short_status")
                    long_price_sps_will = self.controller.model.last_bid_price * self.controller.model.gap_reverse_long
                    print("W shortStatus do short profit status")


            while long_profit_status and self.controller.model.stop_bot_by_stop_button is False:
                print("\nJestesmy w long profit status 2s przerwy")
                time.sleep(self.controller.model.refresh_time)
                dict_future = obj_ftx_methods.get_future(self.controller.model.market_name)
                self.controller.model.last_ask_price = dict_future["ask"]
                self.controller.model.last_bid_price = dict_future["bid"]
                current_ask_decrease = self.controller.model.last_ask_price * self.controller.model.gap_profit_short
                self.controller.model.running_result = Test.calculate_running_result(self.controller.model.last_entry_price,self.controller.model.last_bid_price,self.controller.model.fee,self.controller.model.last_long_or_short)
                self.view.running_result_var.set(str(self.controller.model.running_result) + " running result in long profit status")
                self.view.total_result_var.set(str(self.controller.model.total_result) + " total result")

                if short_price_lps_will < current_ask_decrease:
                    short_price_lps_will = current_ask_decrease

                # trejdd short
                if self.controller.model.last_bid_price <= short_price_lps_will:
                    short_status = True
                    long_profit_status = False

                    self.controller.model.previous_entry_price = self.controller.model.last_entry_price
                    self.controller.model.last_entry_price = self.controller.model.last_bid_price
                    self.controller.model.last_long_or_short = "short"

                    self.controller.model.long_price_will = self.controller.model.last_ask_price * self.controller.model.gap_reverse_long
                    self.view.prices_will_var.set("Prices will "+ str(self.controller.model.long_price_will) + " " + str(self.controller.model.short_price_will))

                    short_profit_price_will = self.controller.model.last_bid_price * self.controller.model.gap_profit_short
                    short_price_lps_will = 0

                    date_time_current = self.dt.datetime.now().replace(microsecond=0)
                    trade = ["short", self.controller.model.last_bid_price, str(date_time_current)]

                    self.controller.model.last_closed_result_no_fee = Test.calculate_last_result_2(self.controller.model.previous_entry_price, self.controller.model.last_entry_price,self.controller.model.last_long_or_short)
                    self.controller.model.total_trades_result = self.controller.model.total_trades_result + self.controller.model.last_closed_result_no_fee
                    self.controller.model.list_of_trades_results.append(self.controller.model.last_closed_result_no_fee)
                    self.controller.model.list_of_trades_total_running_results.append(self.controller.model.total_trades_result)
                    self.controller.model.sum_of_fees = self.controller.model.sum_of_fees + self.controller.model.fee*2
                    self.controller.model.total_result = -self.controller.model.sum_of_fees + self.controller.model.total_trades_result

                    trade.append(self.controller.model.last_closed_result_no_fee)
                    trade.append(self.controller.model.total_result)
                    trade.append(self.controller.model.final_session_result)

                    self.controller.model.list_of_trades.append(trade)
                    self.controller.model.last_trade = trade

            while short_profit_status and self.controller.model.stop_bot_by_stop_button is False:
                print(" \nJestesmy w short profit status 2s przerwy")
                time.sleep(self.controller.model.refresh_time)
                dict_future = obj_ftx_methods.get_future(self.controller.model.market_name)
                self.controller.model.last_ask_price = dict_future["ask"]
                self.controller.model.last_bid_price = dict_future["bid"]
                self.controller.model.running_result = Test.calculate_running_result(self.controller.model.last_entry_price,self.controller.model.last_ask_price,self.controller.model.fee,self.controller.model.last_long_or_short)
                self.view.running_result_var.set(str(self.controller.model.running_result) + " running result in short profit status")
                self.view.total_result_var.set(str(self.controller.model.total_result) + " total result")
                current_bid_increased = self.controller.model.last_bid_price * self.controller.model.gap_reverse_long
                if current_bid_increased < long_price_sps_will:
                    long_price_sps_will = current_bid_increased

                # trejdd long
                if self.controller.model.last_ask_price > long_price_sps_will:
                    long_status = True
                    short_profit_status = False

                    self.controller.model.previous_entry_price = self.controller.model.last_entry_price
                    self.controller.model.last_entry_price = self.controller.model.last_ask_price
                    self.controller.model.last_long_or_short = "long"

                    self.controller.model.short_price_will = self.controller.model.last_ask_price * self.controller.model.gap_profit_short
                    self.view.prices_will_var.set("Prices will "+ str(self.controller.model.long_price_will) + " " + str(self.controller.model.short_price_will))

                    long_profit_price_will = self.controller.model.last_ask_price * self.controller.model.gap_profit_long
                    long_price_sps_will = 0

                    date_time_current = self.dt.datetime.now().replace(microsecond=0)
                    trade = ["long", self.controller.model.last_ask_price, str(date_time_current)]


                    self.controller.model.last_closed_result_no_fee = Test.calculate_last_result_2(self.controller.model.previous_entry_price,self.controller.model.last_entry_price, self.controller.model.last_long_or_short)
                    self.controller.model.total_trades_result = self.controller.model.total_trades_result + self.controller.model.last_closed_result_no_fee
                    self.controller.model.list_of_trades_results.append(self.controller.model.last_closed_result_no_fee)
                    self.controller.model.list_of_trades_total_running_results.append(self.controller.model.total_trades_result)
                    self.controller.model.sum_of_fees = self.controller.model.sum_of_fees + self.controller.model.fee*2
                    self.controller.model.total_result = -self.controller.model.sum_of_fees + self.controller.model.total_trades_result

                    trade.append(self.controller.model.last_closed_result_no_fee)
                    trade.append(self.controller.model.total_result)
                    trade.append(self.controller.model.final_session_result)


                    self.controller.model.list_of_trades.append(trade)
                    self.controller.model.last_trade = trade
                #while stop_bot_by_stop_button:
                    #pass
                #while #stop_bot_by_indicator:
                    #pass

        date_time_current = self.dt.datetime.now().replace(microsecond=0)
        trade = 0
        if self.controller.model.last_long_or_short == 'short':
            trade = ["ClosedShortNoPosition", self.controller.model.last_ask_price, str(date_time_current)]
            self.controller.model.last_long_or_short = "long"
        elif self.controller.model.last_long_or_short == 'long':
            trade = ["ClosedLongNoPosition", self.controller.model.last_bid_price, str(date_time_current)]
            self.controller.model.last_long_or_short = "short"

        self.controller.model.previous_entry_price = self.controller.model.last_entry_price
        self.controller.model.last_entry_price = trade[1]
        self.controller.model.last_closed_result_no_fee = Test.calculate_last_result_2(self.controller.model.previous_entry_price, self.controller.model.last_entry_price,self.controller.model.last_long_or_short)
        self.controller.model.total_trades_result = self.controller.model.total_trades_result + self.controller.model.last_closed_result_no_fee
        self.controller.model.list_of_trades_results.append(self.controller.model.last_closed_result_no_fee)
        self.controller.model.list_of_trades_total_running_results.append(self.controller.model.total_trades_result)
        self.controller.model.sum_of_fees = self.controller.model.sum_of_fees + self.controller.model.fee
        self.controller.model.total_result = -self.controller.model.sum_of_fees + self.controller.model.total_trades_result
        self.controller.model.final_session_result=self.controller.model.total_result

        trade.append(self.controller.model.last_closed_result_no_fee)
        trade.append(self.controller.model.total_result)
        trade.append(self.controller.model.final_session_result)

        self.controller.model.list_of_trades.append(trade)
        self.controller.model.last_trade = trade

        print(str(self.controller.model.last_closed_result_no_fee) +" last closed result ")
        print(str(self.controller.model.final_session_result) + " final session result ")
        print(trade)

        #zapisuje dane do csv
        self.controller.save_file_to_csv()

        self.controller.model.stop_bot_by_stop_button = False
        self.controller.model.list_of_trades = []
        self.controller.model.final_session_result=0
