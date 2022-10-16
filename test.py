import pandas as pd
class Test:

    @staticmethod
    def calculate_results (list_results_my:list):
        counter = 0
        previous_trade = 0
        net_profit=[]
        for x in list_results_my:
            if counter==0:
                previous_trade = x
                counter+=1
                net_profit.append(0)
                continue
            prc_change =x[1] / previous_trade[1]
            if x[0]=="short":
                net_profit.append(prc_change-1)
            if x[0]=="long":
                net_profit.append(1-prc_change)
            #print(str(prc_change) + " prcchange")
            #print(str(net_profit) + " net_profit")
            #print(str(previous_trade)+ " previus x")
            #print(str(x)+ " current x")
            previous_trade =x
        return net_profit

    @staticmethod  #zrobić żeby od tyłu obliczała tylko dwie wartośći - wtedy program jest szybszy
    def calculate_last_result(list_of_trades: list):
        #zwrócić dwie ostatnie wartości tablicy żeby nie iterować za dużo
        counter = 0
        previous_trade = 0
        last_result=0
        for x in list_of_trades:
            if counter == 0:
                previous_trade = x
                counter += 1
                last_result=0
                continue
            prc_change = x[1] / previous_trade[1]
            if x[0] == "short":
                last_result=prc_change - 1
            if x[0] == "long":
                last_result=1 - prc_change
            # print(str(prc_change) + " prcchange")
            # print(str(net_profit) + " net_profit")
            # print(str(previous_trade)+ " previus x")
            # print(str(x)+ " current x")
            previous_trade = x
        return last_result

    @staticmethod
    def calculate_last_result_2(previuos_entry_price, last_entry_price, long_or_short):
        result = 0.0
        if (long_or_short == "long" and previuos_entry_price!=0):
            result=1-(last_entry_price/previuos_entry_price)
        elif (long_or_short == "short" and previuos_entry_price!=0):
            result=1-(previuos_entry_price/last_entry_price)

        print(result)
        return result


    @staticmethod
    def write_list_to_panda_frame_stat(list_my):
        df = pd.DataFrame(columns=['trade','price', 'startDate and time', 'lastTradeResult','totalResult', 'finalSessionResult'])

        counter=0
        for x in list_my:
            df.loc[counter]=x
            counter+=1

        return df

    @staticmethod
    def calculate_running_result (entry_price,last_price, fee:float, long_or_short:str):

        prc_change = 0
        if long_or_short=="long":
            prc_change=last_price/entry_price
        elif long_or_short=="short":
            prc_change=entry_price/last_price  #wynik zawsze na plusie daje plu jeśli minus to minus


        return prc_change-fee-1



    @staticmethod
    def sum_results(list_of_results:list):
        sum_of_results = []
        suma=0
        for x in list_of_results:
            suma=suma+x
            sum_of_results.append(suma)
        return sum_of_results

    @staticmethod
    def sort_dict(d: dict):
        new_dict = sorted(d.items(), key=lambda x: x[1], reverse=True)
        return new_dict


    @staticmethod
    def get_highest_vol_dict(list_of_dict:list):
        highest_vol_dict = {}
        highest_volatility_1h = 0
        market_name = ""
        for x in list_of_dict:
            if abs(x['change1h']) > abs(highest_volatility_1h):
                highest_volatility_1h = x['change1h']
                #market_name = x['name']
                print(x['change1h'])
                print(x['name'])
                highest_vol_dict = x
        return highest_vol_dict

    @staticmethod
    def get_list_of_markets_name(list_of_dict: list):
        list_of_markets = []
        for x in list_of_dict:
            list_of_markets.append(x['name'])
        return list_of_markets

    @staticmethod
    def get_list_of_enabled_perp_dict(list_of_dict: list):
        new_list_of_dict=[]
        substring = "PERP"
        for x in list_of_dict:
            if substring in x['name'] and x['enabled'] == True:
                new_list_of_dict.append(x)

        return new_list_of_dict

    @staticmethod
    def get_list_dict_volatility_1h_restricted(list_of_dict: list, min_volatility: float):
        new_list_of_dict = []
        for x in list_of_dict:
            if min_volatility < abs(x['change1h']):
                new_list_of_dict.append(x)
                print(x)
        return new_list_of_dict








