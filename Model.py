from Bot import Bot_class

#model to czyste dane
class Model:
    def __init__(self):
        self.value = ''
        self.market_name=""
        self.gap_reverse_long = 0.0
        self.gap_reverse_short = 0.0
        self.gap_profit_long = 0.0
        self.gap_profit_short = 0.0
        self.refresh_time = 0
        self.fee = 0.0

        self.starting_date = 0
        self.list_of_trades=[]
        self.last_closed_result_no_fee = 0


    def storing_starting_settings_in_model(self, market_name, gap_reverse_long, gap_reverse_short, gap_profit_long, gap_profit_short, refresh_time, fee):
        self.market_name=str(market_name)
        self.gap_reverse_long = float(gap_reverse_long)
        self.gap_reverse_short = float(gap_reverse_short)
        self.gap_profit_long = float(gap_profit_long)
        self.gap_profit_short = float (gap_profit_short)
        self.refresh_time = int(refresh_time)
        self.fee = float (fee)



