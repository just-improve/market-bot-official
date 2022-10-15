import time

from View import View
from pool_executor import thread_pool_executor, submit_to_pool_executor
from test import Test
import datetime
import tkinter as tk
from tkinter import *

from Ftx_methods import FtxClientWJ


class Bot_class:

    def __init__(self, gap_long, gap_short, gap_profit_long, gap_profit_short, refresh_time, fee: float , view, controller):
        self.controller = controller
        self.view = view
        self.dt = datetime


    def __del__(self):
        print("")


    def get_future_with_1h_vol(self):
        not_found_volatilty_market = True
        pos_or_neg = None
        highest_vol_dict = {}
        while not_found_volatilty_market:
            time.sleep(2)
            obj_ftx_methods = FtxClientWJ()  #Na pewno to jest potrzebne
            #min_change_1h = 0.02
            all_futures = obj_ftx_methods.get_all_futures()
            #print(all_futures)
            perp_list_of_dict = Test.get_list_of_enabled_perp_dict(all_futures)
            list_of_dict_vol_1h_rest = Test.get_list_dict_volatility_1h_restricted(perp_list_of_dict, self.controller.model.min_vol_1h)
            print(list_of_dict_vol_1h_rest)
            highest_vol_dict = Test.get_highest_vol_dict(list_of_dict_vol_1h_rest)
            print(" highest vol dict below")
            print(highest_vol_dict)

            dict_vol_found = bool(highest_vol_dict)
            if dict_vol_found and self.controller.model.previous_market_name == highest_vol_dict['name']:
                if self.controller.model.previous_long_or_short=="long" and highest_vol_dict['change1h']>0 or self.controller.model.previous_long_or_short=="short" and highest_vol_dict['change1h']<0:
                    print("ten sam coin grany powtórka replay wiaderny")
                    print(highest_vol_dict['name'])
                    continue
            #if self.controller.model.previous_long_or_short=="long",

            if bool(highest_vol_dict):
                not_found_volatilty_market = False
                print("mariusz")
                if highest_vol_dict['change1h']>0:
                    pos_or_neg = 1
                elif highest_vol_dict['change1h']<0:
                    pos_or_neg = -1

            #print(highest_vol_dict['name'])
        return highest_vol_dict['name'],highest_vol_dict['change1h'], pos_or_neg

    @submit_to_pool_executor(thread_pool_executor)
    def start_bot2(self):
        obj_ftx_methods = FtxClientWJ()  #Na pewno to jest potrzebne
        mainWhile = True
        isVolatility = False
        after_stoploss_status = False
        long_status = False
        short_status = False
        long_profit_status = False
        short_profit_status = False

        long_price_will = 0
        short_price_will = 0
        long_profit_price_will = 0
        short_profit_price_will = 0
        short_price_lps_will = 0
        long_price_sps_will = 0

        counter_of_trades = 0

        while mainWhile:
            print("mainwhile")
            while isVolatility is False:

                #ta metoda to pętla i jeśli jest zmienność to zwraca market i 1 lub -1, tu musi zwrócić jeszcze zmienność 1h albo stworzyć model class nową z wartościami trejdu, bo za chwilę możemy dodać rsi volume24h i inne
                self.controller.model.market_name, self.controller.model.change1h, pos_or_neg  = self.get_future_with_1h_vol()

                if pos_or_neg == 1:
                    counter_of_trades = 0
                    long_status = True
                    isVolatility = True
                    counter_of_trades=counter_of_trades+1

                    dict_future = obj_ftx_methods.get_future(self.controller.model.market_name)
                    self.controller.model.last_ask_price = dict_future["ask"]
                    self.controller.model.last_bid_price = dict_future["bid"]
                    self.controller.model.last_entry_price = self.controller.model.last_ask_price
                    self.controller.model.last_long_or_short = "long"

                    long_price_will = 0
                    short_price_will = self.controller.model.last_ask_price * self.controller.model.gap_reverse_short
                    long_profit_price_will = self.controller.model.last_ask_price * self.controller.model.gap_profit_long
                    short_profit_price_will = 0
                    long_price_sps_will = 0
                    short_price_lps_will = 0

                    date_time_current = self.dt.datetime.now().replace(microsecond=0)
                    self.controller.model.trade = [self.controller.model.change1h, str(date_time_current), self.controller.model.market_name,self.controller.model.last_long_or_short, self.controller.model.last_entry_price]
                #short
                elif pos_or_neg == -1:
                    counter_of_trades = 0
                    short_status = True
                    isVolatility = True
                    counter_of_trades=counter_of_trades+1

                    dict_future = obj_ftx_methods.get_future(self.controller.model.market_name)
                    self.controller.model.last_ask_price = dict_future["ask"]
                    self.controller.model.last_bid_price = dict_future["bid"]

                    self.controller.model.last_entry_price = self.controller.model.last_bid_price
                    self.controller.model.last_long_or_short = 'short'

                    long_price_will = self.controller.model.last_bid_price * self.controller.model.gap_reverse_long
                    short_price_will = 0
                    long_profit_price_will = 0
                    short_profit_price_will = self.controller.model.last_bid_price * self.controller.model.gap_profit_short
                    long_price_sps_will = 0
                    short_price_lps_will = 0

                    date_time_current = self.dt.datetime.now().replace(microsecond=0)
                    self.controller.model.trade = [self.controller.model.change1h, str(date_time_current), self.controller.model.market_name,self.controller.model.last_long_or_short, self.controller.model.last_entry_price ]

            while isVolatility is True:

                while long_status:
                    time.sleep(self.controller.model.refresh_time)
                    dict_future = obj_ftx_methods.get_future(self.controller.model.market_name)
                    self.controller.model.last_ask_price = dict_future["ask"]
                    self.controller.model.last_bid_price = dict_future["bid"]

                    self.view.running_result_var.set(str(short_price_will) + " short_price_will")
                    self.view.total_result_var.set(str(long_profit_price_will) + " long_profit_price_will")
                    self.view.list_of_trades_var.set(str(self.controller.model.trade) + " trade")
                    self.view.prices_will_var.set(str(self.controller.model.last_bid_price) + str(self.controller.model.last_ask_price) + " bid-ask " +self.controller.model.market_name)
                    self.view.status_info_var.set(" ls "+str(long_status) + " ss "+ str(short_status) + " lps " +str(long_profit_status) + " sps " +str(short_profit_status)+ " ass "+str(after_stoploss_status)+ " is_vol " + str(isVolatility))

                    isVolatility = False
                    after_stoploss_status = False
                    long_status = False
                    short_status = False
                    long_profit_status = False
                    short_profit_status = False

                    # zamkniecie longa stoploss
                    if self.controller.model.last_bid_price <= short_price_will:
                        long_status = False
                        short_status = False
                        after_stoploss_status = True
                        self.controller.model.last_closed_price = self.controller.model.last_bid_price

                        date_time_current = self.dt.datetime.now().replace(microsecond=0)
                        self.controller.model.trade.append(str(date_time_current))
                        self.controller.model.trade.append(self.controller.model.last_closed_price)
                        self.controller.model.trade.append("loose")
                        self.controller.model.list_of_trades.append(self.controller.model.trade)

                    elif self.controller.model.last_ask_price >= long_profit_price_will:
                        long_profit_status = True
                        long_status = False
                        short_price_lps_will = self.controller.model.last_ask_price * self.controller.model.gap_profit_short

                while short_status:
                    time.sleep(self.controller.model.refresh_time)
                    dict_future = obj_ftx_methods.get_future(self.controller.model.market_name)
                    self.controller.model.last_ask_price = dict_future["ask"]
                    self.controller.model.last_bid_price = dict_future["bid"]

                    self.view.running_result_var.set(str(long_price_will )+ " long_price_will"  )
                    self.view.total_result_var.set(str(short_profit_price_will) + " short_profit_price_will")
                    self.view.list_of_trades_var.set(str(self.controller.model.trade) + " trade")
                    self.view.prices_will_var.set(str(self.controller.model.last_bid_price) + str(self.controller.model.last_ask_price) + " bid-ask " +self.controller.model.market_name)
                    self.view.status_info_var.set(" ls "+str(long_status) + " ss "+ str(short_status) + " lps " +str(long_profit_status) + " sps " +str(short_profit_status)+ " ass "+str(after_stoploss_status)+ " is_vol " + str(isVolatility))

                    #zamkniecie shorta stoploss
                    if self.controller.model.last_ask_price > long_price_will:
                        long_status = False
                        short_status = False
                        after_stoploss_status = True
                        self.controller.model.last_closed_price = self.controller.model.last_ask_price

                        date_time_current = self.dt.datetime.now().replace(microsecond=0)

                        self.controller.model.trade.append(str(date_time_current))
                        self.controller.model.trade.append(self.controller.model.last_closed_price)
                        self.controller.model.trade.append("loose")
                        self.controller.model.list_of_trades.append(self.controller.model.trade)

                        counter_of_trades = counter_of_trades + 1

                    elif self.controller.model.last_bid_price < short_profit_price_will:
                        short_profit_status = True
                        short_status = False
                        long_price_sps_will = self.controller.model.last_bid_price * self.controller.model.gap_reverse_long

                while long_profit_status:
                    time.sleep(self.controller.model.refresh_time)
                    dict_future = obj_ftx_methods.get_future(self.controller.model.market_name)
                    self.controller.model.last_ask_price = dict_future["ask"]
                    self.controller.model.last_bid_price = dict_future["bid"]
                    current_ask_decrease = self.controller.model.last_ask_price * self.controller.model.gap_profit_short

                    self.view.running_result_var.set(str(short_price_lps_will )+ " short_price_lps_will"  )
                    #self.view.total_result_var.set(str(short_profit_price_will) + " short_profit_price_will")
                    self.view.list_of_trades_var.set(str(self.controller.model.trade) + " trade")
                    self.view.prices_will_var.set(str(self.controller.model.last_bid_price) + str(self.controller.model.last_ask_price) + " bid-ask " +self.controller.model.market_name)
                    self.view.status_info_var.set(" ls "+str(long_status) + " ss "+ str(short_status) + " lps " +str(long_profit_status) + " sps " +str(short_profit_status)+ " ass "+str(after_stoploss_status)+ " is_vol " + str(isVolatility))

                    # update ceny wejścia w short gdy cena rośnie
                    if short_price_lps_will < current_ask_decrease:
                        short_price_lps_will = current_ask_decrease

                    # wejście w short z long profit statusu
                    if self.controller.model.last_bid_price <= short_price_lps_will:
                        short_status = False
                        long_profit_status = False
                        after_stoploss_status = True

                        self.controller.model.last_closed_price = self.controller.model.last_bid_price

                        date_time_current = self.dt.datetime.now().replace(microsecond=0)
                        self.controller.model.trade.append(str(date_time_current))
                        self.controller.model.trade.append(self.controller.model.last_closed_price)
                        self.controller.model.trade.append("win")
                        self.controller.model.list_of_trades.append(self.controller.model.trade)

                while short_profit_status:
                    time.sleep(self.controller.model.refresh_time)
                    dict_future = obj_ftx_methods.get_future(self.controller.model.market_name)
                    self.controller.model.last_ask_price = dict_future["ask"]
                    self.controller.model.last_bid_price = dict_future["bid"]
                    current_bid_increased = self.controller.model.last_bid_price * self.controller.model.gap_reverse_long

                    self.view.running_result_var.set(str(long_price_sps_will )+ " long_price_sps_will"  )
                    #self.view.total_result_var.set(str(short_profit_price_will) + " short_profit_price_will")
                    self.view.list_of_trades_var.set(str(self.controller.model.trade) + " trade")
                    self.view.prices_will_var.set(str(self.controller.model.last_bid_price) + str(self.controller.model.last_ask_price) + " bid-ask " +self.controller.model.market_name)
                    self.view.status_info_var.set(" ls "+str(long_status) + " ss "+ str(short_status) + " lps " +str(long_profit_status) + " sps " +str(short_profit_status)+ " ass "+str(after_stoploss_status)+ " is_vol " + str(isVolatility))

                    #update ceny wejścia w long gdy cena spada
                    if current_bid_increased < long_price_sps_will:
                        long_price_sps_will = current_bid_increased

                    #wejście w long z short profit statusu
                    if self.controller.model.last_ask_price > long_price_sps_will:
                        short_status = False
                        short_profit_status = False
                        after_stoploss_status = True

                        self.controller.model.last_closed_price = self.controller.model.last_ask_price

                        date_time_current = self.dt.datetime.now().replace(microsecond=0)
                        self.controller.model.trade.append(str(date_time_current))
                        self.controller.model.trade.append(self.controller.model.last_closed_price)
                        self.controller.model.trade.append("win")
                        self.controller.model.list_of_trades.append(self.controller.model.trade)

                while after_stoploss_status:
                    print("after stop loss")
                    print(self.controller.model.list_of_trades)
                    self.view.status_info_var.set(" ls "+str(long_status) + " ss "+ str(short_status) + " lps " +str(long_profit_status) + " sps " +str(short_profit_status)+ " ass "+str(after_stoploss_status)+ " is_vol " + str(isVolatility))
                    #trzeba by wykluczyć ten sm kierunek trejdu w taki spósób że trzeba by stworzyć zmienną która sprawdzana by była przez metodę
                    self.controller.model.previous_market_name = self.controller.model.market_name
                    self.controller.model.previous_long_or_short = self.controller.model.last_long_or_short


                    self.controller.model.market_name = ""
                    self.controller.model.trade = []
                    self.controller.model.last_long_or_short = ""
                    self.controller.model.last_ask_price = 0.0
                    self.controller.model.last_bid_price = 0.0


                    isVolatility = False
                    after_stoploss_status = False
                    long_status = False
                    short_status = False
                    long_profit_status = False
                    short_profit_status = False

                    short_price_will = 0
                    long_profit_price_will = 0
                    long_price_will = 0
                    short_profit_price_will = 0
                    long_price_sps_will = 0
                    short_price_lps_will = 0

                    #short_price_will = self.controller.model.last_ask_price * self.controller.model.gap_reverse_short
                    #long_profit_price_will = self.controller.model.last_ask_price * self.controller.model.gap_profit_long
                    #long_price_will = 0
                    #short_profit_price_will = 0
                    #long_price_sps_will = 0
                    #short_price_lps_will = 0




