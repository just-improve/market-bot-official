from Bot import Bot_class
from Model import Model
from View import View


class Controller:

    def __init__(self):
        self.view = View(self)
        self.model = Model()

    def main(self):
        self.view.main()

    def start_bot(self):
        self.model.storing_starting_settings_in_model(self.view.market_name_entry.get(), self.view.gap_reverse_long_entry.get(), self.view.gap_reverse_short_entry.get(), self.view.gap_profit_long_entry.get(), self.view.gap_profit_short_entry.get(), self.view.refresh_time_entry.get(), self.view.market_fee_entry.get())
        obj = Bot_class(self.model.market_name, self.model.gap_reverse_long, self.model.gap_reverse_short, self.model.gap_profit_long,
                        self.model.gap_profit_short, self.model.refresh_time, self.model.fee, self.view, self)
        obj.start_bot()

    def on_button_click_stop_program(self):
        self.view.quit()

if __name__ == '__main__':

    controller_instance = Controller()
    controller_instance.main()
