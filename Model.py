from Bot import Bot_class

#model to czyste dane
class Model:
    def __init__(self):
        self.value = ''
        self.starting_date = 0
        self.list_of_trades=[]
        self.last_closed_result_no_fee = 0
        self.total_trades_result = 0
        self.list_of_trades_results=[]
        self.list_of_trades_total_running_results = []
        self.sum_of_fees = 0
        self.total_result = 0
        self.running_result = 0
        self.last_entry_price = 0
        self.last_long_or_short = None
        self.long_price_will = 0
        self.short_price_will = 0



    def storing_starting_settings_in_model(self, market_name, gap_reverse_long, gap_reverse_short, gap_profit_long, gap_profit_short, refresh_time, fee):
        self.market_name=str(market_name)
        self.gap_reverse_long = float(gap_reverse_long)
        self.gap_reverse_short = float(gap_reverse_short)
        self.gap_profit_long = float(gap_profit_long)
        self.gap_profit_short = float (gap_profit_short)
        self.refresh_time = int(refresh_time)
        self.fee = float (fee)



