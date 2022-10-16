import time

from Market import MarketModel
from View import View
from pool_executor import thread_pool_executor, submit_to_pool_executor
from test import Test
import datetime
import tkinter as tk
from tkinter import *

from Ftx_methods import FtxClientWJ


class Bot_class:

    def __init__(self , view, controller):
        self.controller = controller
        self.view = view
        self.dt = datetime
        self.list_of_obj_markets = []
        self.list_of_playing_obj_markets = []
        self.list_of_all_trades = []


    def creating_list_obj(self):
        obj_ftx_methods = FtxClientWJ()
        all_futures = obj_ftx_methods.get_all_futures()
        perp_list_of_dict = Test.get_list_of_enabled_perp_dict(all_futures)
        list_of_markets = Test.get_list_of_markets_name(perp_list_of_dict)
        for x in list_of_markets:
            objMarket = MarketModel(x)
            self.list_of_obj_markets.append(objMarket)

    def setting_starting_coins(self):
        at_least_one_coin_is_playing = True
        while at_least_one_coin_is_playing:
            time.sleep(1)
            print("in method setting_starting_coins ")
            obj_ftx_methods = FtxClientWJ()
            all_futures = obj_ftx_methods.get_all_futures()
            perp_list_of_dict = Test.get_list_of_enabled_perp_dict(all_futures)
            for x in perp_list_of_dict:
                for y in self.list_of_obj_markets:
                    if x['name'] == y.market_name:
                        if abs(x['change1h']) > float(self.controller.view.min_vol_1h_entry.get()):
                            y.change1h = x['change1h']
                            y.is_playing=True
                            at_least_one_coin_is_playing = False

                            if x['change1h']>0:
                                y.status = "long"
                                y.entry_price = x['ask']
                                y.bid = x['bid']
                                y.ask = x['ask']
                                y.short_price_will = x['ask']*self.controller.model.gap_reverse_short
                                y.stoploss_price_will = x['ask'] * self.controller.model.gap_reverse_short
                                y.long_profit_price_will = x['bid']*self.controller.model.gap_profit_long
                                y.start_trade_time = "15;00"

                            elif x['change1h']<0:
                                y.status = "short"
                                y.entry_price = x['bid']
                                y.bid = x['bid']
                                y.ask = x['ask']
                                y.long_price_will = x['bid']*self.controller.model.gap_reverse_long
                                y.stoploss_price_will = x['bid']*self.controller.model.gap_reverse_long
                                y.short_profit_price_will = x['ask']*self.controller.model.gap_profit_short
                                y.start_trade_time = "18;00"

    def get_list_of_playing_obj_markets(self):
        list_of_played_markets = []
        for x in self.list_of_obj_markets:
            if x.is_playing:
                list_of_played_markets.append(x)
        return list_of_played_markets

    def get_list_of_playing_obj_from_ftx(self, obj_ftx_methods):
        all_futures = obj_ftx_methods.get_all_futures()
        list_of_played_market_with_new_data = []
        for x in all_futures:
            for y in self.list_of_playing_obj_markets:
                if y.market_name == x['name']:
                    list_of_played_market_with_new_data.append(x)
        return list_of_played_market_with_new_data

    def print_details_of_obj_list(self, obj_list):
        for x in obj_list:
            print("")
            list_as_str = ""
            list_of_fileds = []
            list_of_fileds.append(str(x.market_name))
            list_of_fileds.append(str(x.change1h) + " change1h")
            list_of_fileds.append(str(len(obj_list)) + " len os playing obj ")
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
            print(list_as_str)


            #print(str(x.market_name) +" "+ str(x.change1h) + " change1h")
            #print(str(x.change1h) + " change1h")
            #print(str(x.list_of_trades) + " list_of_trades")
            #print(str(len(obj_list)) + " len os playing obj ")
            #print(str(x.won_or_lost) + " won_or_lost")
            #print(str(x.is_playing) + " is playing")
            #print(str(x.status) + " status")
            #print(str(x.bid) + " " + str(x.ask) + " aski bidy")
            #print(str(x.entry_price) + " entry_price")

            #print(str(x.closed_price) + " closed_price")
            #print(str(x.stoploss_price_will) + " stoploss_price_will")
            #print(str(x.long_profit_price_will) + " long_profit_price_will")
            #print(str(x.short_profit_price_will) + " short_profit_price_will")

            f = open("demofile.txt", 'a')
            f.write(list_as_str+'\n')

    def update_status_only_close(self, obj_ftx_methods):
        list_of_playing_obj_from_ftx = self.get_list_of_playing_obj_from_ftx(obj_ftx_methods)

        #in long stop loss go to stoploss
        for x in list_of_playing_obj_from_ftx:
            for y in self.list_of_playing_obj_markets:
                if y.market_name == x['name'] and y.status == "long" and y.is_playing == True:
                    y.bid = x['bid']
                    y.ask = x['ask']
                    if y.stoploss_price_will > x['bid']:
                        y.is_playing = False
                        y.status = "no"
                        y.won_or_lost = "lost"
                        y.closed_price = x['bid']
                        y.last_long_or_short = "long"
                        y.end_trade_time = "9;000"
                        y.create_trade_fileds_store_in_list_trades()
                        self.list_of_all_trades.append(y.trade)
                        y.reset_obj_data_fields()

                    #long_profit
                    elif y.long_profit_price_will < x['ask']:
                        print("long_profit enter " + str(y.long_profit_price_will) + " y.long_profit price przed edycją " + str(x['ask']) + " ask ")
                        y.status = "long_profit"
                        #wiaderny
                        y.stoploss_price_will = x['ask'] * self.controller.model.gap_reverse_short
                        print("long_profit enter " + str(y.stoploss_price_will) + " y.stoploss_price_will nowy")
                        y.long_profit_price_will = 0.0

            #in short stop loss go to stoploss
            for x in list_of_playing_obj_from_ftx:
                for y in self.list_of_playing_obj_markets:
                    if y.market_name == x['name'] and y.status == "short" and y.is_playing == True:
                        y.bid = x['bid']
                        y.ask = x['ask']
                        if y.long_price_will < x['ask']:
                            y.is_playing = False
                            y.status = "no"
                            y.won_or_lost = "lost"
                            y.closed_price = x['ask']
                            y.last_long_or_short = "short"
                            y.end_trade_time = "11;00s"
                            y.create_trade_fileds_store_in_list_trades()
                            self.list_of_all_trades.append(y.trade)
                            y.reset_obj_data_fields()

                        #short_profit
                        elif y.short_profit_price_will > x['bid']:
                            print("short_profit enter " + str(y.short_profit_price_will) + " y.short_profit_price_will przed edycją " + str(x['bid']) + " bid " )
                            y.status = "short_profit"
                            y.stoploss_price_will = x['bid'] * self.controller.model.gap_reverse_long
                            print("short_profit enter " + str(y.stoploss_price_will) + " y.stoploss_price_will po edycji")
                            y.short_profit_price_will = 0.0

            #for coins in long_profit go to trailingstop won
            for x in list_of_playing_obj_from_ftx:
                for y in self.list_of_playing_obj_markets:
                    if y.market_name == x['name'] and y.status == "long_profit":
                        y.bid = x['bid']
                        y.ask = x['ask']
                        if y.stoploss_price_will > x['bid']:
                            y.is_playing = False
                            y.status = "no"
                            y.won_or_lost = "won"
                            y.closed_price = x['bid']
                            y.last_long_or_short = "long"
                            y.create_trade_fileds_store_in_list_trades()
                            self.list_of_all_trades.append(y.trade)
                            y.reset_obj_data_fields()

                        #update ceny long_profit_status
                        elif x['ask'] * self.controller.model.gap_reverse_short < y.stoploss_price_will:
                            y.stoploss_price_will = x['ask'] * self.controller.model.gap_reverse_short
                            print("update long_profit price " + str(y.stoploss_price_will))

            #for coins in short_profit go to trailingstop won
            for x in list_of_playing_obj_from_ftx:
                for y in self.list_of_playing_obj_markets:
                    if y.market_name == x['name'] and y.status == "short_profit":
                        y.bid = x['bid']
                        y.ask = x['ask']
                        if y.stoploss_price_will < x['ask']:
                            y.is_playing = False
                            y.status = "no"
                            y.won_or_lost = "won"
                            y.closed_price = x['ask']
                            y.last_long_or_short = "short"
                            y.create_trade_fileds_store_in_list_trades()
                            self.list_of_all_trades.append(y.trade)
                            y.reset_obj_data_fields()

                        #update ceny short_profit status
                        elif y.stoploss_price_will > x['bid'] * self.controller.model.gap_reverse_long:
                             y.stoploss_price_will = x['bid'] * self.controller.model.gap_reverse_long
                             print("update short_profit price " + str(y.stoploss_price_will))
                             #printer_fileds(y) przydała by się metoda która drukuje tylko pola jednego obiektu


    @submit_to_pool_executor(thread_pool_executor)
    def start_bot_group(self):
        obj_ftx_methods = FtxClientWJ()
        self.creating_list_obj()
        self.setting_starting_coins()
        self.list_of_playing_obj_markets = self.get_list_of_playing_obj_markets()
        self.print_details_of_obj_list(self.list_of_playing_obj_markets)
        while 1:
            time.sleep(10)
            # po co jest ta metoda? po co mi ta lista tutaj?
            #self.list_of_playing_obj_markets = self.get_list_of_playing_obj_markets()
            self.update_status_only_close(obj_ftx_methods)
            print(self.list_of_all_trades)
            #self.print_details_of_obj_list(self.list_of_playing_obj_markets)




    #nie używane metody
    def update_status (self, obj_ftx_methods):
        list_of_playing_obj_from_ftx = self.get_list_of_playing_obj_from_ftx(obj_ftx_methods)

        #for coins in long stop loss go to short
        for x in list_of_playing_obj_from_ftx:
            for y in  self.list_of_playing_obj_markets:
                if y.market_name == x['name'] and y.status=="long":
                    if y.short_price_will > x['bid']:
                        y.status = "short"
                        y.entry_price = x['bid']
                        y.long_price_will = x['bid'] * self.controller.model.gap_reverse_long
                        y.short_profit_price_will = x['ask'] * self.controller.model.gap_profit_short
                    elif y.long_profit_price_will < x['ask']:
                        y.status = "long_profit"
                        y.short_price_will = x['ask']*self.controller.model.gap_reverse_short

            #for coins in short stop loss go to long
            for x in list_of_playing_obj_from_ftx:
                for y in self.list_of_playing_obj_markets:
                    if y.market_name == x['name'] and y.status == "short":
                        if y.long_price_will < x['ask']:
                            y.status = "long"
                            y.entry_price = x['ask']
                            y.short_price_will = x['ask'] * self.controller.model.gap_reverse_short
                            y.long_profit_price_will = x['bid'] * self.controller.model.gap_profit_long
                        elif y.short_profit_price_will>x['bid']:
                            y.status="short_profit"
                            y.long_price_will = x['bid']*self.controller.model.gap_profit_long
