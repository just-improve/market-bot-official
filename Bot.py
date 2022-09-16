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
        self.gap_long = gap_long
        self.gap_short = gap_short
        self.gap_profit_long = gap_profit_long
        self.gap_profit_short = gap_profit_short
        self.market = market
        self.last_closed_result=0    # jest kalkulowany bez fee
        self.total_trades_result = 0
        self.list_of_trades_results = []
        self.list_of_trades_total_running_results = []
        self.fee=fee
        self.sum_of_fees=0
        self.total_result=0
        self.running_result = 0
        self.last_entry_price=0
        self.last_long_or_short = None


    def __del__(self):
        print("")

    @submit_to_pool_executor(thread_pool_executor)
    def start_bot(self):
        obj_ftx_methods = FtxClientWJ()

        first_price = obj_ftx_methods.get_future(self.market)["bid"]
        prc_init_long = 1.0001  # jedna dziesiąta procenta zmiany ceny
        prc_init_short = 0.9999  # jedna dziesiąta procenta zmiany ceny    zmiana ceny o 20 $ około

        long_price_sps_will = 0
        short_price_lps_will = 0

        long_price_will = first_price * prc_init_long
        short_price_will = first_price * prc_init_short

        long_profit_price_will = 0
        short_profit_price_will = 0
        main_while = False
        long_status = False
        short_status = False
        long_profit_status = False
        short_profit_status = False
        initialize_while = True

        # pętla inicjalizująca w celu wszedł w jakąś pozycję
        while initialize_while:
            print("\n petla inicializująca   ")
            #self.view.gap_reverse_short_entry.insert(0,"dashjkdshs")
            time.sleep(self.controller.model.refresh_time)
            bid_last = obj_ftx_methods.get_future(self.market)["bid"]
            ask_last = obj_ftx_methods.get_future(self.market)["ask"]
            self.view.running_result_var.set(str(self.running_result) + " running result init")
            self.view.total_result_var.set(str(self.total_result) + " total result")
            if ask_last >= long_price_will:
                initialize_while = False
                long_status = True
                main_while = True
                print(ask_last)
                print(bid_last)
                print("long entry initialize")
                date_time_current = self.dt.datetime.now().replace(microsecond=0)
                trade = ("long", ask_last, str(date_time_current), self.market)

                self.last_entry_price=ask_last
                self.last_long_or_short = "long"
                self.controller.model.list_of_trades.append(trade)
                long_price_will = 0
                short_profit_price_will = 0
                long_profit_price_will = ask_last * self.gap_profit_long
                short_price_will = ask_last * self.gap_short

                self.last_closed_result = Test.calculate_last_result(self.controller.model.list_of_trades)
                self.total_trades_result = self.total_trades_result + self.last_closed_result
                self.list_of_trades_results.append(self.last_closed_result)
                self.list_of_trades_total_running_results.append(self.total_trades_result)
                self.sum_of_fees = self.sum_of_fees + self.fee
                self.total_result=-self.sum_of_fees + self.total_trades_result

            elif bid_last <= short_price_will:
                initialize_while = False
                short_status = True
                main_while = True
                print("short entry initialize")

                date_time_current = self.dt.datetime.now().replace(microsecond=0)
                trade = ("short", bid_last, str(date_time_current), self.market)
                #trade = ("short", ask_last)
                self.last_entry_price=ask_last
                self.last_long_or_short = "short"
                self.controller.model.list_of_trades.append(trade)

                long_price_will = bid_last * self.gap_long
                short_profit_price_will = bid_last * self.gap_profit_short
                long_profit_price_will = 0
                short_price_will = 0


                self.last_closed_result = Test.calculate_last_result(self.controller.model.list_of_trades)
                self.total_trades_result = self.total_trades_result + self.last_closed_result

                self.list_of_trades_results.append(self.last_closed_result)

                self.list_of_trades_total_running_results.append(self.total_trades_result)

                self.sum_of_fees = self.sum_of_fees + self.fee

                self.total_result = -self.sum_of_fees + self.total_trades_result
                #self.create_entry_in_bot()


        while main_while:
            time.sleep(0.1)

            while long_status:
                print("\nLong status and now pause 2sec")
                time.sleep(self.controller.model.refresh_time)
                dict_future = obj_ftx_methods.get_future(self.market)
                ask_last = dict_future["ask"]
                bid_last = dict_future["bid"]
                self.running_result = Test.calculate_running_result(self.last_entry_price,bid_last,self.fee,self.last_long_or_short)
                self.view.running_result_var.set(str(self.controller.model.refresh_time) + " running result in long")
                self.view.total_result_var.set(str(self.controller.model.list_of_trades) + " total result")

                if bid_last <= short_price_will:
                    long_status = False
                    short_status = True
                    print("trejd short_status z long_status ")
                    long_price_will = ask_last * self.gap_long
                    short_profit_price_will = bid_last * self.gap_profit_short
                    long_profit_price_will = 0
                    short_price_will = 0

                    date_time_current = self.dt.datetime.now().replace(microsecond=0)
                    trade = ("short", bid_last, str(date_time_current), self.market)

                    self.last_entry_price = bid_last
                    self.last_long_or_short = "short"

                    self.controller.model.list_of_trades.append(trade)

                    print("W Long status do shortStatus")

                    self.last_closed_result = Test.calculate_last_result(self.controller.model.list_of_trades)
                    self.total_trades_result = self.total_trades_result + self.last_closed_result

                    self.list_of_trades_results.append(self.last_closed_result)

                    self.list_of_trades_total_running_results.append(self.total_trades_result)

                    self.sum_of_fees = self.sum_of_fees + self.fee*2

                    self.total_result = -self.sum_of_fees + self.total_trades_result


                elif ask_last >= long_profit_price_will:
                    long_profit_status = True
                    long_status = False
                    print("trejd long_profit_status z long_status")

                    long_profit_price_will = 0
                    long_profit_price_will = 0
                    long_price_will = 0
                    short_price_will = ask_last * self.gap_short
                    short_price_lps_will = ask_last * self.gap_short
                    print("W LongStatus do LongProfitStatus ")

            while short_status:
                print("\nShort status and now pause 2sec")
                time.sleep(self.controller.model.refresh_time)
                dict_future = obj_ftx_methods.get_future(self.market)
                ask_last = dict_future["ask"]
                bid_last = dict_future["bid"]
                self.running_result = Test.calculate_running_result(self.last_entry_price,ask_last,self.fee,self.last_long_or_short)
                self.view.running_result_var.set(str(self.running_result) + " running result in short")
                self.view.total_result_var.set(str(self.controller.model.list_of_trades) + " total result")

                if ask_last > long_price_will:
                    long_status = True
                    short_status = False
                    print("trejd long_status z short_status")
                    short_profit_price_will = 0
                    short_price_will = bid_last * self.gap_short
                    long_profit_price_will = ask_last * self.gap_profit_long

                    date_time_current = self.dt.datetime.now().replace(microsecond=0)
                    trade = ("long", ask_last, str(date_time_current), self.market)

                    self.last_entry_price = ask_last
                    self.last_long_or_short = "long"

                    self.controller.model.list_of_trades.append(trade)

                    print("W shortStatus do longStatus")

                    self.last_closed_result = Test.calculate_last_result(self.controller.model.list_of_trades)
                    self.total_trades_result = self.total_trades_result + self.last_closed_result
                    self.list_of_trades_results.append(self.last_closed_result)
                    self.list_of_trades_total_running_results.append(self.total_trades_result)
                    self.sum_of_fees = self.sum_of_fees + self.fee*2
                    self.total_result = -self.sum_of_fees + self.total_trades_result

                elif bid_last < short_profit_price_will:
                    short_profit_status = True
                    short_status = False
                    print("trejd short_profit_status z short_status")
                    long_price_sps_will = bid_last * self.gap_long
                    print("W shortStatus do short profit status")


            while long_profit_status:
                print("\nJestesmy w long profit status 2s przerwy")
                time.sleep(self.controller.model.refresh_time)
                dict_future = obj_ftx_methods.get_future(self.market)
                ask_last = dict_future["ask"]
                bid_last = dict_future["bid"]
                current_ask_decrease = ask_last * self.gap_short
                self.running_result = Test.calculate_running_result(self.last_entry_price,bid_last,self.fee,self.last_long_or_short)
                self.view.running_result_var.set(str(self.running_result) + " running result in long profit status")
                self.view.total_result_var.set(str(self.total_result) + " total result")



                if short_price_lps_will < current_ask_decrease:
                    short_price_lps_will = current_ask_decrease

                if bid_last <= short_price_lps_will:
                    print("trejd short_status z long_profit_status")
                    short_status = True
                    long_profit_status = False
                    long_price_will = ask_last * self.gap_long
                    short_profit_price_will = bid_last * self.gap_profit_short
                    short_price_lps_will = 0

                    date_time_current = self.dt.datetime.now().replace(microsecond=0)
                    trade = ("short", bid_last, str(date_time_current), self.market)

                    self.last_entry_price = bid_last
                    self.last_long_or_short = "short"
                    self.controller.model.list_of_trades.append(trade)


                    self.last_closed_result = Test.calculate_last_result(self.controller.model.list_of_trades)
                    self.total_trades_result = self.total_trades_result + self.last_closed_result

                    self.list_of_trades_results.append(self.last_closed_result)

                    self.list_of_trades_total_running_results.append(self.total_trades_result)

                    self.sum_of_fees = self.sum_of_fees + self.fee*2

                    self.total_result = -self.sum_of_fees + self.total_trades_result

            while short_profit_status:
                print(" \nJestesmy w short profit status 2s przerwy")
                time.sleep(self.controller.model.refresh_time)
                dict_future = obj_ftx_methods.get_future(self.market)
                ask_last = dict_future["ask"]
                bid_last = dict_future["bid"]
                self.running_result = Test.calculate_running_result(self.last_entry_price,ask_last,self.fee,self.last_long_or_short)
                self.view.running_result_var.set(str(self.running_result) + " running result in short profit status")
                self.view.total_result_var.set(str(self.total_result) + " total result")

                current_bid_increased = bid_last * self.gap_long

                if current_bid_increased < long_price_sps_will:
                    long_price_sps_will = current_bid_increased

                if ask_last > long_price_sps_will:
                    long_status = True
                    short_profit_status = False
                    print("trejd long_status z  short_profit_status")

                    short_price_will = ask_last * self.gap_short
                    long_profit_price_will = ask_last * self.gap_profit_long

                    date_time_current = self.dt.datetime.now().replace(microsecond=0)
                    trade = ("long", ask_last, str(date_time_current), self.market)

                    self.last_entry_price = ask_last
                    self.last_long_or_short = "long"
                    print("W short profit go to longStatus")
                    self.controller.model.list_of_trades.append(trade)
                    self.last_closed_result = Test.calculate_last_result(self.controller.model.list_of_trades)
                    self.total_trades_result = self.total_trades_result + self.last_closed_result
                    self.list_of_trades_results.append(self.last_closed_result)
                    self.list_of_trades_total_running_results.append(self.total_trades_result)
                    self.sum_of_fees = self.sum_of_fees + self.fee*2
                    self.total_result = -self.sum_of_fees + self.total_trades_result
