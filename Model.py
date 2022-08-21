from Bot import Bot_class



#model to czyste dane
class Model:
    def __init__(self):
        self.value = ''

    def calculate(self):
        print("in model calculate " )

    def calculate_with_argument(self, text):
        print(text)

    def creating_bot_instance(self, market_name, gap_reverse_long,gap_reverse_short, gap_profit_long, gap_profit_short, refresh_time, fee ):

        market_name=str(market_name)
        gap_reverse_long = float(gap_reverse_long)
        gap_reverse_short = float(gap_reverse_short)
        gap_profit_long = float(gap_profit_long)
        gap_profit_short = float (gap_profit_short)
        refresh_time = int(refresh_time)
        fee = float (fee)
        obj = Bot_class( market_name, gap_reverse_long, gap_reverse_short, gap_profit_long, gap_profit_short, refresh_time, fee)
        obj.start_bot()
        print("controller test branch")
        print("controller test branch222")
        print("in creating_bot_instance")

