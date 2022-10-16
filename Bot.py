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
        self.list_of_playing_markets = []


    def print_all_obj_with_all_data(self):
        for x in self.list_of_obj_markets:
            if x.entry_price !=0:
                print(str(x.entry_price) + x.market_name)
            if x.long_price_will !=0:
                print(str(x.long_price_will) + " "+ x.market_name)


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
            obj_ftx_methods = FtxClientWJ()
            all_futures = obj_ftx_methods.get_all_futures()
            perp_list_of_dict = Test.get_list_of_enabled_perp_dict(all_futures)
            for x in perp_list_of_dict:
                for y in self.list_of_obj_markets:
                    if x['name'] == y.market_name:
                        if abs(x['change1h']) > 0.01:
                            y.change1h = x['change1h']
                            y.is_playing=True
                            at_least_one_coin_is_playing = False

                            if x['change1h']>0:
                                y.status = "long"
                                y.entry_price = x['ask']
                                y.short_price_will = x['ask']*self.controller.model.gap_reverse_short
                                y.stoploss_price_will = x['ask'] * self.controller.model.gap_reverse_short
                                y.long_profit_price_will = x['bid']*self.controller.model.gap_profit_long

                            elif x['change1h']<0:
                                y.status = "short"
                                y.entry_price = x['bid']
                                y.long_price_will = x['bid']*self.controller.model.gap_reverse_long
                                y.stoploss_price_will = x['bid']*self.controller.model.gap_reverse_long
                                y.short_profit_price_will = x['ask']*self.controller.model.gap_profit_short

    def get_list_of_playing_obj_markets(self):
        list_of_played_markets = []
        for x in self.list_of_obj_markets:
            if x.is_playing:
                list_of_played_markets.append(x)
        return list_of_played_markets

    def print_market_name_of_obj_list(self, obj_list):
        for x in obj_list:
            print("")
            print(x.market_name)
            print(x.status)
            print(str(x.stoploss_price_will) + " stoploss_price_will")


    def get_list_of_playing_obj_from_ftx(self, obj_ftx_methods):
        all_futures = obj_ftx_methods.get_all_futures()
        list_of_played_market_with_new_data = []
        for x in all_futures:
            for y in self.list_of_playing_markets:
                if y.market_name == x['name']:
                    list_of_played_market_with_new_data.append(x)
        return list_of_played_market_with_new_data

    def update_status (self, obj_ftx_methods):
        list_of_playing_obj_from_ftx = self.get_list_of_playing_obj_from_ftx(obj_ftx_methods)

        #for coins in long stop loss go to short
        for x in list_of_playing_obj_from_ftx:
            for y in  self.list_of_playing_markets:
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
                for y in self.list_of_playing_markets:
                    if y.market_name == x['name'] and y.status == "short":
                        if y.long_price_will < x['ask']:
                            y.status = "long"
                            y.entry_price = x['ask']
                            y.short_price_will = x['ask'] * self.controller.model.gap_reverse_short
                            y.long_profit_price_will = x['bid'] * self.controller.model.gap_profit_long
                        elif y.short_profit_price_will>x['bid']:
                            y.status="short_profit"
                            y.long_price_will = x['bid']*self.controller.model.gap_profit_long

    def update_status_only_close(self, obj_ftx_methods):
        list_of_playing_obj_from_ftx = self.get_list_of_playing_obj_from_ftx(obj_ftx_methods)

        #in long stop loss go to stoploss
        for x in list_of_playing_obj_from_ftx:
            for y in self.list_of_playing_markets:
                if y.market_name == x['name'] and y.status == "long" and y.is_playing == True:
                    if y.stoploss_price_will > x['bid']:
                        y.is_playing = False
                        y.status = "no"
                        y.won_or_lost = "lost"
                        y.closed_price = x['bid']
                        y.last_long_or_short = "long"
                        y.store_trade_in_list()
                        y.reset_data()

                    #long_profit
                    elif y.long_profit_price_will < x['ask']:
                        y.status = "long_profit"
                        y.stoploss_price_will = x['ask'] * self.controller.model.gap_reverse_short

            #in short stop loss go to stoploss
            for x in list_of_playing_obj_from_ftx:
                for y in self.list_of_playing_markets:
                    if y.market_name == x['name'] and y.status == "short" and y.is_playing == True:
                        if y.long_price_will < x['ask']:
                            y.is_playing = False
                            y.status = "no"
                            y.won_or_lost = "lost"
                            y.closed_price = x['ask']
                            y.last_long_or_short = "short"
                            y.store_trade_in_list()
                            y.reset_data()

                        #short_profit
                        elif y.short_profit_price_will > x['bid']:
                            y.status = "short_profit"
                            y.stoploss_price_will = x['bid'] * self.controller.model.gap_reverse_long

            #for coins in long_profit go to trailingstop won
            for x in list_of_playing_obj_from_ftx:
                for y in self.list_of_playing_markets:
                    if y.market_name == x['name'] and y.status == "long_profit":
                        if y.stoploss_price_will > x['bid']:
                            y.is_playing = False
                            y.status = "no"
                            y.won_or_lost = "won"
                            y.closed_price = x['bid']
                            y.last_long_or_short = "long"
                            y.store_trade_in_list()
                            y.reset_data()

                        #update ceny long_profit status
                        elif x['ask'] * self.controller.model.gap_reverse_short < y.stoploss_price_will:
                            y.stoploss_price_will = x['ask'] * self.controller.model.gap_reverse_short

            #for coins in short_profit go to trailingstop won
            for x in list_of_playing_obj_from_ftx:
                for y in self.list_of_playing_markets:
                    if y.market_name == x['name'] and y.status == "short_profit":
                        if y.stoploss_price_will < x['ask']:
                            y.is_playing = False
                            y.status = "no"
                            y.won_or_lost = "won"
                            y.closed_price = x['ask']
                            y.last_long_or_short = "short"
                            y.store_trade_in_list()
                            y.reset_data()

                        #update ceny short_profit status
                        elif y.stoploss_price_will > x['bid'] * self.controller.model.gap_reverse_long:
                             y.stoploss_price_will = x['bid'] * self.controller.model.gap_reverse_long




    @submit_to_pool_executor(thread_pool_executor)
    def start_bot_group(self):
        obj_ftx_methods = FtxClientWJ()
        self.creating_list_obj()
        self.setting_starting_coins()
        self.list_of_playing_markets = self.get_list_of_playing_obj_markets()
        self.print_market_name_of_obj_list(self.list_of_playing_markets)
        while 1:
            time.sleep(2)
            self.list_of_playing_markets = self.get_list_of_playing_obj_markets()
            self.print_market_name_of_obj_list(self.list_of_playing_markets)
            self.update_status_only_close(obj_ftx_methods)

