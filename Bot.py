import time

from test import Test
import datetime
import tkinter as tk
from tkinter import *

from Ftx_methods import FtxClientWJ


class Bot_class:

    #root = Tk()


    #def create_entry_in_bot(self):

        #b1 = Button(self.root, text="Next")
        #b1.pack()
        #text_result = ttk.text(self.main_frame, justify='right')
        #text_result.insert(0, "bllll")
        #text_result.pack()

    def __init__(self, market: str, gap_long, gap_short, gap_profit_long, gap_profit_short, refresh_time, fee: float ):
        #self.controller = controller
        self.dt = datetime
        self.time_sleep=refresh_time
        self.gap_long = gap_long
        self.gap_short = gap_short
        self.gap_profit_long = gap_profit_long
        self.gap_profit_short = gap_profit_short
        self.market = market
        self.list_of_tup_trades=[]
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


    def print_my_variables (self):
        print(str (self.gap_long)  + " self.gap_long")
        print(str (self.gap_short)  + " self.gap_short")
        print(str (self.gap_profit_long) + " self.gap_profit_long")
        print(str (self.gap_profit_short ) + " self.gap_profit_short")
        print(str (self.market ) + " self.market")
        print(str (self.market ) + " self.market")
        print(str (self.list_of_tup_trades) + " self.list_of_tup_trades"  )
        print(str (self.last_closed_result) + " self.last_result")
        print(str (self.list_of_trades_results ) + " self.list_of_trades_results " )
        print(str (self.list_of_trades_total_running_results) + " self.list_of_trades_total_running_results"  )
        print(str (self.fee) + " self.fee=fee" )
        print(str (self.sum_of_fees) + " self.sum_of_fees" )
        print(str (self.total_trades_result) +" self.total_trades_result" )
        print(str (self.total_result) + " self.total_result" )
        print(str (self.running_result) + " self.running_result " )



    def __del__(self):
        Bot_class.print_my_variables(self)

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

        trade = ()

        print(type(self.list_of_tup_trades))
        print(long_price_will)
        print(short_price_will)
        print(str(first_price) + " first_price  ")

        # pętla inicjalizująca w celu wszedł w jakąś pozycję
        while initialize_while:
            print("\n petla inicializująca   ")
            #self.view.gap_reverse_short_entry.insert(0,"dashjkdshs")
            time.sleep(self.time_sleep)
            bid_last = obj_ftx_methods.get_future(self.market)["bid"]
            ask_last = obj_ftx_methods.get_future(self.market)["ask"]
            print(str(ask_last) + " ask_last  ")
            print(str(bid_last) + " bid_last  ")
            print(str(long_price_will) + " long_price_will")
            print(str(short_price_will)+ " short_price_will")

            if ask_last >= long_price_will:
                initialize_while = False
                long_status = True
                main_while = True
                print(ask_last)
                print(bid_last)
                print("long entry initialize")
                date_time_current = self.dt.datetime.now().replace(microsecond=0)
                trade = ("long", ask_last, str(str(date_time_current)))

                self.last_entry_price=ask_last
                self.last_long_or_short = "long"
                self.list_of_tup_trades.append(trade)
                print(self.list_of_tup_trades)
                long_price_will = 0
                short_profit_price_will = 0
                long_profit_price_will = ask_last * self.gap_profit_long
                short_price_will = ask_last * self.gap_short

                self.last_closed_result = Test.calculate_last_result(self.list_of_tup_trades)
                self.total_trades_result = self.total_trades_result + self.last_closed_result
                print(str(self.last_closed_result) + " last_result")
                print(str(self.total_trades_result) + " total_trades_result")

                self.list_of_trades_results.append(self.last_closed_result)
                print(str(self.list_of_trades_results) + " list_of_trades_results")

                self.list_of_trades_total_running_results.append(self.total_trades_result)
                print(str(self.list_of_trades_total_running_results) + " list_of_trades_running_results")

                self.sum_of_fees = self.sum_of_fees + self.fee
                print(str(self.sum_of_fees) + " sum_of_fees")

                self.total_result=-self.sum_of_fees + self.total_trades_result
                print(str(self.total_result) + " total_result")

                #self.create_entry_in_bot()


            elif bid_last <= short_price_will:
                initialize_while = False
                short_status = True
                main_while = True
                print(ask_last)
                print(bid_last)
                print("short entry initialize")

                date_time_current = self.dt.datetime.now().replace(microsecond=0)
                trade = ("short", bid_last, str(str(date_time_current)))
                #trade = ("short", ask_last)
                self.last_entry_price=ask_last
                self.last_long_or_short = "short"
                self.list_of_tup_trades.append(trade)
                print(self.list_of_tup_trades)
                long_price_will = bid_last * self.gap_long
                short_profit_price_will = bid_last * self.gap_profit_short
                long_profit_price_will = 0
                short_price_will = 0


                self.last_closed_result = Test.calculate_last_result(self.list_of_tup_trades)
                self.total_trades_result = self.total_trades_result + self.last_closed_result
                print(str(self.last_closed_result) + " last_result")
                print(str(self.total_trades_result) + " total_trades_result")

                self.list_of_trades_results.append(self.last_closed_result)
                print(str(self.list_of_trades_results) + " list_of_trades_results")

                self.list_of_trades_total_running_results.append(self.total_trades_result)
                print(str(self.list_of_trades_total_running_results) + " list_of_trades_running_results")

                self.sum_of_fees = self.sum_of_fees + self.fee
                print(str(self.sum_of_fees) + " sum_of_fees")

                self.total_result = -self.sum_of_fees + self.total_trades_result
                print(str(self.total_result) + " total_result")
                #self.create_entry_in_bot()


        while main_while:
            time.sleep(0.1)

            while long_status:
                print("\nLong status and now pause 2sec")
                time.sleep(self.time_sleep)
                dict_future = obj_ftx_methods.get_future(self.market)
                ask_last = dict_future["ask"]
                bid_last = dict_future["bid"]
                print(str(self.list_of_tup_trades) + " self.list_of_tup_trades")
                self.running_result = Test.calculate_running_result(self.last_entry_price,bid_last,self.fee,self.last_long_or_short)
                print(str(self.running_result)+" self.running_result")
                print(str(self.total_result) + " total_result")

                print(ask_last)
                print(bid_last)
                print(str(long_profit_price_will) + " long_profit_price_will w longStatus")
                print(str(short_price_will) + " short_price_will w longStatus")

                if bid_last <= short_price_will:
                    long_status = False
                    short_status = True
                    print("trejd short_status z long_status ")
                    long_price_will = ask_last * self.gap_long
                    short_profit_price_will = bid_last * self.gap_profit_short
                    long_profit_price_will = 0
                    short_price_will = 0

                    date_time_current = self.dt.datetime.now().replace(microsecond=0)
                    trade = ("short", bid_last, str(str(date_time_current)))

                    self.last_entry_price = bid_last
                    self.last_long_or_short = "short"

                    self.list_of_tup_trades.append(trade)
                    print("W Long statusu do shortStatus")
                    print(self.list_of_tup_trades)

                    self.last_closed_result = Test.calculate_last_result(self.list_of_tup_trades)
                    self.total_trades_result = self.total_trades_result + self.last_closed_result
                    print(str(self.last_closed_result) + " last_result")
                    print(str(self.total_trades_result) + " total_trades_result")

                    self.list_of_trades_results.append(self.last_closed_result)
                    print(str(self.list_of_trades_results) + " list_of_trades_results")

                    self.list_of_trades_total_running_results.append(self.total_trades_result)
                    print(str(self.list_of_trades_total_running_results) + " list_of_trades_running_results")

                    self.sum_of_fees = self.sum_of_fees + self.fee*2
                    print(str(self.sum_of_fees) + " sum_of_fees")

                    self.total_result = -self.sum_of_fees + self.total_trades_result
                    print(str(self.total_result) + " total_result")


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
                time.sleep(self.time_sleep)
                dict_future = obj_ftx_methods.get_future(self.market)
                ask_last = dict_future["ask"]
                bid_last = dict_future["bid"]
                print(str(self.list_of_tup_trades) + " self.list_of_tup_trades")
                self.running_result = Test.calculate_running_result(self.last_entry_price,ask_last,self.fee,self.last_long_or_short)
                print(str(self.running_result)+" self.running_result")
                print(str(self.total_result) + " total_result")


                print(ask_last)
                print(bid_last)
                print(str(short_profit_price_will) + " short_profit_price_will w statusieShort")
                print(str(long_price_will) + " long_price_will w statusieShort")

                if ask_last > long_price_will:
                    long_status = True
                    short_status = False
                    print("trejd long_status z short_status")
                    short_profit_price_will = 0
                    short_price_will = bid_last * self.gap_short
                    long_profit_price_will = ask_last * self.gap_profit_long

                    date_time_current = self.dt.datetime.now().replace(microsecond=0)
                    trade = ("long", ask_last, str(date_time_current))

                    self.last_entry_price = ask_last
                    self.last_long_or_short = "long"

                    self.list_of_tup_trades.append(trade)
                    print("W shortStatus do longStatus")
                    print(self.list_of_tup_trades)

                    self.last_closed_result = Test.calculate_last_result(self.list_of_tup_trades)
                    self.total_trades_result = self.total_trades_result + self.last_closed_result
                    print(str(self.last_closed_result) + " last_result")
                    print(str(self.total_trades_result) + " total_trades_result")

                    self.list_of_trades_results.append(self.last_closed_result)
                    print(str(self.list_of_trades_results) + " list_of_trades_results")

                    self.list_of_trades_total_running_results.append(self.total_trades_result)
                    print(str(self.list_of_trades_total_running_results) + " list_of_trades_running_results")

                    self.sum_of_fees = self.sum_of_fees + self.fee*2
                    print(str(self.sum_of_fees) + " sum_of_fees")

                    self.total_result = -self.sum_of_fees + self.total_trades_result
                    print(str(self.total_result) + " total_result")

                elif bid_last < short_profit_price_will:
                    short_profit_status = True
                    short_status = False
                    print("trejd short_profit_status z short_status")
                    long_price_sps_will = bid_last * self.gap_long
                    print("W shortStatus do short profit status")

                    # short_profit_price_will

                # print(self.list_of_tup_trades[len(self.list_of_tup_trades)-1])

            while long_profit_status:
                print("\nJestesmy w long profit status 2s przerwy")
                time.sleep(self.time_sleep)
                dict_future = obj_ftx_methods.get_future(self.market)
                ask_last = dict_future["ask"]
                bid_last = dict_future["bid"]
                print(str(self.list_of_tup_trades) + " self.list_of_tup_trades")
                current_ask_decrease = ask_last * self.gap_short
                print(ask_last)
                print(bid_last)
                self.running_result = Test.calculate_running_result(self.last_entry_price,bid_last,self.fee,self.last_long_or_short)
                print(str(self.running_result)+" self.running_result")
                print(str(self.total_result) + " total_result")



                print(str(short_price_lps_will) + " short_price_lps_will przed ")
                if short_price_lps_will < current_ask_decrease:
                    short_price_lps_will = current_ask_decrease
                print(str(short_price_lps_will) + " short_price_lps_will po ")

                if bid_last <= short_price_lps_will:
                    print("trejd short_status z long_profit_status")
                    short_status = True
                    long_profit_status = False
                    long_price_will = ask_last * self.gap_long
                    short_profit_price_will = bid_last * self.gap_profit_short
                    short_price_lps_will = 0

                    date_time_current = self.dt.datetime.now().replace(microsecond=0)
                    trade = ("short", bid_last, str(date_time_current))

                    self.last_entry_price = bid_last
                    self.last_long_or_short = "short"
                    self.list_of_tup_trades.append(trade)
                    print(self.list_of_tup_trades)

                    self.last_closed_result = Test.calculate_last_result(self.list_of_tup_trades)
                    self.total_trades_result = self.total_trades_result + self.last_closed_result
                    print(str(self.last_closed_result) + " last_result")
                    print(str(self.total_trades_result) + " total_trades_result")

                    self.list_of_trades_results.append(self.last_closed_result)
                    print(str(self.list_of_trades_results) + " list_of_trades_results")

                    self.list_of_trades_total_running_results.append(self.total_trades_result)
                    print(str(self.list_of_trades_total_running_results) + " list_of_trades_running_results")

                    self.sum_of_fees = self.sum_of_fees + self.fee*2
                    print(str(self.sum_of_fees) + " sum_of_fees")

                    self.total_result = -self.sum_of_fees + self.total_trades_result
                    print(str(self.total_result) + " total_result")

            while short_profit_status:
                print(" \nJestesmy w short profit status 2s przerwy")
                time.sleep(self.time_sleep)
                dict_future = obj_ftx_methods.get_future(self.market)
                ask_last = dict_future["ask"]
                bid_last = dict_future["bid"]
                print(str(self.list_of_tup_trades) + " self.list_of_tup_trades")
                self.running_result = Test.calculate_running_result(self.last_entry_price,ask_last,self.fee,self.last_long_or_short)
                print(str(self.running_result)+" self.running_result")
                print(str(self.total_result) + " total_result")


                print(ask_last)
                print(bid_last)
                current_bid_increased = bid_last * self.gap_long

                print(str(long_price_sps_will) + " long_price_sps_will przed ")
                if current_bid_increased < long_price_sps_will:
                    long_price_sps_will = current_bid_increased
                print(str(long_price_sps_will) + " long_price_sps_will po  ")

                if ask_last > long_price_sps_will:
                    long_status = True
                    short_profit_status = False
                    print("trejd long_status z  short_profit_status")

                    short_price_will = ask_last * self.gap_short
                    long_profit_price_will = ask_last * self.gap_profit_long

                    date_time_current = self.dt.datetime.now().replace(microsecond=0)
                    trade = ("long", ask_last, str(date_time_current))

                    self.last_entry_price = ask_last
                    self.last_long_or_short = "long"

                    print("W short profit go to longStatus")

                    self.list_of_tup_trades.append(trade)
                    print(self.list_of_tup_trades)

                    self.last_closed_result = Test.calculate_last_result(self.list_of_tup_trades)
                    self.total_trades_result = self.total_trades_result + self.last_closed_result
                    print(str(self.last_closed_result) + " last_result")
                    print(str(self.total_trades_result) + " total_trades_result")

                    self.list_of_trades_results.append(self.last_closed_result)
                    print(str(self.list_of_trades_results) + " list_of_trades_results")

                    self.list_of_trades_total_running_results.append(self.total_trades_result)
                    print(str(self.list_of_trades_total_running_results) + " list_of_trades_running_results")

                    self.sum_of_fees = self.sum_of_fees + self.fee*2
                    print(str(self.sum_of_fees) + " sum_of_fees")

                    self.total_result = -self.sum_of_fees + self.total_trades_result
                    print(str(self.total_result) + " total_result")