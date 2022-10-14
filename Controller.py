import csv
import pandas as pd
from Bot import Bot_class
from Model import Model
from View import View
from test import Test


class Controller:

    def __init__(self):
        self.view = View(self)
        self.model = Model()

    def main(self):
        self.view.main()

    def start_bot(self):

        self.model.storing_starting_settings_in_model(self.view.market_name_entry.get(),self.view.gap_reverse_long_init.get(),self.view.gap_reverse_short_init.get(), self.view.gap_reverse_long_entry.get(), self.view.gap_reverse_short_entry.get(), self.view.gap_profit_long_entry.get(), self.view.gap_profit_short_entry.get(), self.view.refresh_time_entry.get(), self.view.market_fee_entry.get())
        obj = Bot_class(self.model.market_name, self.model.gap_reverse_long, self.model.gap_reverse_short, self.model.gap_profit_long,
                        self.model.gap_profit_short, self.model.refresh_time, self.model.fee, self.view, self)

        obj.start_bot2()


    def save_file_to_csv(self):
        df = Test.write_list_to_panda_frame_stat(self.model.list_of_trades)
        df.to_csv(self.model.market_name + ".csv", mode='a',index=False, header=False)
        print(df)

    def on_button_click_while_bot_stop(self):
        self.model.stop_bot_by_stop_button=True

    def list_as_string_in_new_line(self, list_to_edit):
        list_as_str_with_new_line = ""
        for x in list_to_edit:
            list_as_str_with_new_line = list_as_str_with_new_line + str(x) + "\n"
        return list_as_str_with_new_line


if __name__ == '__main__':

    controller_instance = Controller()
    controller_instance.main()
