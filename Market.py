
class MarketModel:
    def __init__(self, name):
        self.status = "no"
        self.is_playing = False
        self.market_name = name
        self.list_of_trades = []
        self.last_long_or_short = None
        self.bid_price = 0.0
        self.ask_price = 0.0
        self.last_entry_price = 0
        self.last_closed_price = 0
        self.change1h = 0.0

        self.long_price_will = 0
        self.short_price_will = 0
        self.long_profit_price_will = 0
        self.short_profit_price_will = 0
        self.short_price_lps_will = 0
        self.long_price_sps_will = 0
        self.counter_of_trades = 0

    def reset_prices(self):
        self.status = "no"
        self.is_playing = False
        self.bid_price = 0.0
        self.ask_price = 0.0
        self.change1h = 0.0

        self.long_price_will = 0
        self.short_price_will = 0
        self.long_profit_price_will = 0
        self.short_profit_price_will = 0
        self.short_price_lps_will = 0
        self.long_price_sps_will = 0
        self.counter_of_trades = 0