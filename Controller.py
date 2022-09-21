import csv
import pandas as pd
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

    def on_button_click_stop_program_and_save(self):
        keys = ['trade', 'price', 'startDate', 'startTime', 'market']
        myvar = pd.DataFrame(keys)
        print(myvar)
        #file_name = self.model.market_name +" "+ self.model.gap_reverse_long +" " +self.model.gap_profit_long+".csv"
        file_name = self.model.market_name+" "+str(self.model.gap_reverse_long)+" "+str(self.model.gap_profit_long)+".csv"
        file = open(file_name, 'w', newline='')
        dict_writer = csv.DictWriter(file, keys)
        #dict_writer.writeheader()
        dict_writer.writerows(self.model.list_of_trades)
        file.close()
        self.view.quit()

    def on_button_click_stop_program_save_to_csv(self):
        #df = pd.DataFrame(columns=['trade','price', 'startDate', 'startTime', 'market'])
        date_start_time = str(self.model.start_time)
        date_end_time = str(self.model.end_time)
        both_dates = date_start_time+" "+date_end_time
        both_dates = both_dates.replace('/','.')
        both_dates = both_dates.replace('-','.')
        both_dates = both_dates.replace(':','.')
        df=self.write_list_to_panda_frame(self.model.list_of_trades)
        df.to_csv(self.model.market_name + " "+both_dates+".csv",index=True)
        print(df)
        self.view.quit()

    def on_button_click_stop_program_and_save_txt(self):
        lis_as_str_new_line = self.list_as_string_in_new_line(self.model.list_of_trades)
        file_name = self.model.market_name+" "+str(self.model.total_result)+".txt"
        file = open(file_name, 'w', newline='')
        file.write(str(self.model.last_trade) + " last trade\n")
        file.write(str(self.model.last_long_or_short) + " last long or short\n")
        file.write(str(self.model.last_entry_price) + " last entry price\n")
        file.write(str(self.model.start_time) + " start time\n")
        file.write(str(self.model.total_result)+ " total result\n")
        file.write(lis_as_str_new_line + "\n")
        file.close()
        self.view.quit()


    #te dwie metody przeniesc do innej klasy
    def write_list_to_panda_frame(self, list_my):
        df = pd.DataFrame(columns=['trade','price', 'startDate and time', 'lastTradeResult','totalResult','previousEntry','lastEntry', 'market'])

        counter=0
        for x in list_my:
            df.loc[counter]=x
            counter+=1

        return df

    def list_as_string_in_new_line(self, list_to_edit):
        list_as_str_with_new_line = ""
        for x in list_to_edit:
            list_as_str_with_new_line = list_as_str_with_new_line + str(x) + "\n"
        return list_as_str_with_new_line


if __name__ == '__main__':

    controller_instance = Controller()
    controller_instance.main()
