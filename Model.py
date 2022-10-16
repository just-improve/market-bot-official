from Bot import Bot_class

#model to czyste dane
class Model:
    def __init__(self):
        self.market_name = ""
        self.gap_reverse_long =0.0
        self.gap_reverse_short =0.0
        self.gap_profit_long =0.0
        self.gap_profit_short =0.0
        self.refresh_time = 2
        self.fee = 0.0
        self.list_of_settings = []
        self.list_of_settings_as_str = ""
        self.min_vol_1h = 0.0

    def storing_starting_settings_in_model(self, minimum_vol_1h, gap_reverse_long, gap_reverse_short, gap_profit_long, gap_profit_short, refresh_time, fee):
        self.min_vol_1h = float(minimum_vol_1h)
        self.gap_reverse_long = float(gap_reverse_long)
        self.gap_reverse_short = float(gap_reverse_short)
        self.gap_profit_long = float(gap_profit_long)
        self.gap_profit_short = float (gap_profit_short)
        self.refresh_time = int(refresh_time)
        self.fee = float (fee)
        self.list_of_settings = [self.market_name,self.gap_reverse_long, self.gap_reverse_short, self.gap_profit_long, self.gap_profit_short, self.refresh_time, self.fee ]
        self.list_of_settings_as_str = " grl "+str(self.gap_reverse_long)+" grs "+ str(self.gap_reverse_short)+" gpl "+ str(self.gap_profit_long)+" gps "+ str(self.gap_profit_short)+" ref_time "+ str(self.refresh_time)+" fee "+ str(self.fee)

class ModelGroup:
    def __init__(self):
        pass
        #self.list_of_obj_markets = []
        #self.list_of_currently_played = []