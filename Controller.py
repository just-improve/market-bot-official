from Bot import Bot_class
from Model import Model
from View import View


class Controller:

    def __init__(self):
        self.view = View(self)
        self.model = Model(self.view)

    def main(self):
        self.view.main()

    def on_button_click(self):
        self.model.creating_bot_instance(self.view.market_name_entry.get(), self.view.gap_reverse_long_entry.get(), self.view.gap_reverse_short_entry.get(), self.view.gap_profit_long_entry.get(), self.view.gap_profit_short_entry.get(), self.view.refresh_time_entry.get(), self.view.market_fee_entry.get())

    def on_button_click_with_argument(self, text):
        self.model.calculate_with_argument(text)

    def on_button_click_stop_program(self):
        self.view.quit()



if __name__ == '__main__':
    print("if main")
    #obj = Bot_class("CEL-PERP",1, 3, 3, 4, 5, 2)   #
    #obj.start_bot()

    calculator = Controller()
    calculator.main()
