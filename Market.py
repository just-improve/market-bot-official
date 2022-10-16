
class MarketModel:
    def __init__(self, name):
        self.status = "no"
        self.is_playing = False
        self.market_name = name
        self.list_of_trades = []
        self.trade = []
        self.last_long_or_short = "no"
        self.entry_price = 0
        self.closed_price = 0
        self.change1h = 0.0
        self.won_or_lost = "no"
        self.start_trade_time = ""
        self.end_trade_time = ""
        self.bid = 0.0
        self.ask = 0.0

        self.stoploss_price_will = 0
        self.long_price_will = 0
        self.short_price_will = 0
        self.long_profit_price_will = 0
        self.short_profit_price_will = 0
        self.short_price_lps_will = 0
        self.long_price_sps_will = 0
        self.counter_of_trades = 0
        self.start_trade_time = ""
        self.end_trade_time = ""

    def reset_obj_data_fields(self):
        print("reset data metod")
        self.status = "no"
        self.is_playing = False
        self.change1h = 0.0

        self.long_price_will = 0
        self.short_price_will = 0
        self.long_profit_price_will = 0
        self.short_profit_price_will = 0
        self.short_price_lps_will = 0
        self.long_price_sps_will = 0
        self.stoploss_price_will = 0
        self.trade = []

    def create_trade_fileds_store_in_list_trades(self):
        self.trade=[self.won_or_lost,self.market_name,self.last_long_or_short, self.entry_price, self.closed_price, self.start_trade_time, self.end_trade_time]
        self.list_of_trades.append(self.trade)
        #print(self.list_of_trades)



        #metoda która drukuje wszystkie obiekty i ich pola ale tylko te pola które mają jakąś wartość