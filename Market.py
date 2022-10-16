
class MarketModel:
    def __init__(self, name):
        self.status = "no"
        self.is_playing = False
        self.market_name = name
        self.list_of_trades = []
        self.last_long_or_short = "no"
        self.entry_price = 0
        self.closed_price = 0
        self.change1h = 0.0
        self.won_or_lost = "no"

        self.stoploss_price_will = 0
        self.long_price_will = 0
        self.short_price_will = 0
        self.long_profit_price_will = 0
        self.short_profit_price_will = 0
        self.short_price_lps_will = 0
        self.long_price_sps_will = 0
        self.counter_of_trades = 0

    def reset_data(self):
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
        self.counter_of_trades = 0

    def store_trade_in_list(self):
        new_list=[self.market_name,self.last_long_or_short, self.entry_price, self.closed_price, self.won_or_lost]
        self.list_of_trades.append(new_list)
        print(self.list_of_trades)



        #metoda która drukuje wszystkie obiekty i ich pola ale tylko te pola które mają jakąś wartość