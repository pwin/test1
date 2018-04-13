# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 14:26:43 2018

@author: pwin
@version: 0.1
@since: 2018-04-13

"""


from io import StringIO
from datetime import datetime, timedelta
import time
import random
import sys
import math

class StockManager():
    def __init__(self):
        """initialise the stock list"""
        self.stock = []
        
    def create_data_file(self):
        """create a file object of a list of comma-delimited stock data"""
        f = StringIO()
        data = """Stock_Symbol,Type,Last_Dividend,Fixed_Dividend,Par_Value
        TEA,Common,0,,100
        POP,Common,8,,100
        ALE,Common,23,,60
        GIN,Preferred,8,.02,100
        JOE,Common,13,,250"""
        f.write(data)
        return f

    def load_data(self, f):
        """load dictionary d with stock data from the list,
        using stock code and stock type to give a key because they might be 'Preferred' or 'Common'"""
        d = {}
        f.seek(0)
        headers = f.readline().strip().split(',')
        for line in f:
            l = line.strip().split(',')
            d[l[0] + '_' + l[1]] = dict((zip(headers,l)))
        return d
    
    def stock_move(self, stock_symbol='', stock_type='', buy_sell= '', number='', trade_price=''):
        """create a stock trade"""
        self.stock.append([stock_symbol, stock_type, buy_sell, number, trade_price, datetime.now()])

    def user_record_trade(self):
        """allow the user to add stock trades for one of the given stocks"""
        f = self.create_data_file()
        d = self.load_data(f)
        stock_keys = d.keys()
        stock_key = [x[:3] for x in list(stock_keys)]
        stock_symbol = ''
        stock_type = ''
        buy_sell = ''
        trade_price = ''
        number = ''
        while True:
            stock_symbol_input = input("Enter one of the following stock codes: {0} >".format(','.join(stock_key)))
            if stock_symbol_input.upper() not in stock_key:
                print("sorry, that was not in the list of available stock")
                continue
            else:
                stock_symbol = stock_symbol_input.upper()
                stock_type = [x for x in list(stock_keys) if x[:3] == stock_symbol][0].split('_')[1]
                break
        while True:
            buy_sell_input = input("Enter 'b' to buy or 's' to sell  ")
            if buy_sell_input.lower() not in ['b', 's']:
                print("sorry, that was not a correct entry.  Please try again")
                continue
            else:
                if buy_sell_input.lower() == 'b':
                    buy_sell = 1
                elif buy_sell_input.lower() == 's':
                    buy_sell = -1
                break
        while True:
            try:
                number_input = int(input("Enter number of stock to trade  "))
            except ValueError:
                print("sorry, that was not a numerical, whole number entry.  Please try again")
                continue
            if number_input < 1:
                print("sorry, your number must not be zero or negative.")
                continue
            else:
                number = number_input
                break
        while True:
            try:
                trade_price_input = int(input("Enter trade price of stock  "))
            except ValueError:
                print("sorry, that was not a numerical, whole number entry.  Please try again")
                continue
            if trade_price_input < 1:
                print("sorry, your number must not be zero or negative.")
                continue
            else:
                trade_price = trade_price_input
                break
        self.stock.append([stock_symbol, stock_type, buy_sell, number, trade_price, datetime.now()])
        print("The following stock data were entered:")
        print(self.stock[-1])
        print("the full stock list is: ")
        print(self.stock)


    def calculate_dividend_yield(self, stock_code, market_price):
        """for a given stock and a market price, returns a dividend yield"""
        dividend_yield = None
        f = self.create_data_file()
        d = self.load_data(f)
        stock_keys = d.keys()
        stock_key = [x for x in list(stock_keys) if x[:3] == stock_code][0]
        try:
            if market_price == 0:
                dividend_yield = float('inf')
            elif d[stock_key]['Type'] == 'Common':
                dividend_yield = float(d[stock_key]['Last_Dividend'])/market_price
            elif d[stock_key]['Type'] == 'Preferred':
                dividend_yield = float(d[stock_key]['Fixed_Dividend']) * float(d[stock_key]['Par_Value']) / market_price
        except Exception as e:
            print('ERROR: ' + str(e))
            dividend_yield = None            
        return dividend_yield



    def calculate_p_e_ratio(self, stock_code, market_price):
        """for a given stock and a market price, returns a p/e ratio"""
        f = self.create_data_file()
        d = self.load_data(f)
        stock_keys = d.keys()
        stock_key = [x for x in list(stock_keys) if x[:3] == stock_code][0]
        print('stock key:  ', stock_key, ' last dividend: ', d[stock_key]['Last_Dividend'])
        try:
            if d[stock_key]['Last_Dividend'] == 0:
                p_e_ratio = float('inf')
            else:
                p_e_ratio = market_price / float(d[stock_key]['Last_Dividend'])
        except Exception as e:
            print('ERROR: ' + str(e))
            p_e_ratio = None
        return p_e_ratio


    def create_rand_stock(self, n):
        """create a random set of n stock entries taking options from the data file"""
        stock_buy_sell = [-1, 1]
        stock_symbols = list(self.load_data(self.create_data_file()).keys())
        stock_number = range(1000)
        stock_price = range(1000)
        
        for i in range(n):
            stock_symbol, stock_type = random.choice(stock_symbols).split('_')
            buy_sell = random.choice(stock_buy_sell)
            number = random.choice(stock_number)
            trade_price = random.choice(stock_price)
            self.stock_move(stock_symbol=stock_symbol, stock_type=stock_type, buy_sell=buy_sell,
                       number=number, trade_price=trade_price)
            if i % 100 == 0:
                print(".", end='')
            time.sleep(1)


    def return_stock_traded_past_t_mins(self, stock_list, stock_code, t):
        """return the stocks traded in the past t minutes"""
        return [x for x in stock_list if x[0] == stock_code and x[5] > datetime.now() - timedelta(minutes=t)]
    
    
    def calculate_volume_weighted_stock_price(self, stock_list, stock_code):
        """calculate the volume-weighted stock price where x[3] = stock_number and x[4] = trade_price"""
        try:
            stocks_selected = self.return_stock_traded_past_t_mins(stock_list, stock_code, 15)
            print(stocks_selected)
            retval = sum([x[3] * x[4] for x in stocks_selected]) / sum([x[3] for x in stocks_selected])
        except Exception as e:
            retval = "Error: " + str(e)
        return retval
    
    
    def calculate_all_share_index(self, stock_list):
        """calculate the all share index using the geometric mean"""
        try:
            all_trade_prices = [x[4] for x in stock_list]
            retval = self.geom_mean(all_trade_prices)
        except Exception as e:
            retval = "Error: " + str(e)
        return retval

    def geom_mean(self, l):
        """geometric mean of a list"""
        try:
            gm = 10 ** (sum([math.log(x, 10) for x in l if x != 0]) / len(l))
        except Exception as e:
            print("ERROR:  " + str(e))
            gm = None
        return gm


       

def main():
    c = StockManager()
    while True:
        option_selected = input("""
Given a market price as input, calculate the dividend yield > 1
Given a market price as input,  calculate the P/E Ratio > 2
Record a trade, with timestamp, quantity of shares, buy or sell indicator and trade price > 3
Calculate Volume Weighted Stock Price based on trades in past 15 minutes > 4
Calculate the GBCE All Share Index using the geometric mean of prices for all stocks > 5

Pick an option [1-5] or 0 to quit
""")
        try:
            if int(option_selected) == 1:
                market_price = input("Enter market price:  ")
                stock_code = input("Enter stock code:  ").upper()
                print("dividend yield:  {0} ".format(c.calculate_dividend_yield(stock_code, float(market_price))))
            elif int(option_selected) == 2:
                market_price = input("Enter market price:  ")
                stock_code = input("Enter stock code:  ").upper()
                print("P/E Ratio:  {0} ".format( c.calculate_p_e_ratio(stock_code, float(market_price))))
            elif int(option_selected) == 3:
                c.user_record_trade()
            elif int(option_selected) == 4:
                existing_or_new = input("Use existing data [e] or wait over 17 minutes and create a new dataset automatically [n]?  enter 'e' or 'n'").lower()
                stock_code = input("Enter stock code:  ").upper()
                t = 15
                if existing_or_new in ['e', 'n']:
                    if existing_or_new == 'e':
                        stock_list = c.stock
                        print("Volume Weighted Stock Price for {0} is {1}".format(stock_code, c.calculate_volume_weighted_stock_price(stock_list, stock_code)))
                    elif existing_or_new == 'n':
                        c.stock = [] # reset
                        c.create_rand_stock(17 * 60) # create 17 minutes of stock trades at 1 per second
                        stock_list = c.stock
                        print("Volume Weighted Stock Price for {0} is {1}".format(stock_code, c.calculate_volume_weighted_stock_price(stock_list, stock_code)))
                else:
                    print("error in entry (should be 'e' or 'n')")
                    continue
            elif int(option_selected) == 5:
                existing_or_new = input("Use existing data [e] or wait over 17 minutes and create a new dataset automatically [n]?  enter 'e' or 'n'").lower()
                t = 15
                if existing_or_new in ['e', 'n']:
                    if existing_or_new == 'e':
                        stock_list = c.stock
                        print("All Share Index is {0}".format(c.calculate_all_share_index(stock_list)))
                    elif existing_or_new == 'n':
                        c.stock = []
                        c.create_rand_stock(17 * 60) #create 17 minutes of stock trades at 1 per second
                        stock_list = c.stock
                        print("All Share Index is {0}".format(c.calculate_all_share_index(stock_list)))
                    else:
                        continue
                else:
                    print("error in entry (should be 'e' or 'n')")
                    continue
            elif int(option_selected) == 0:
                sys.exit()
        except Exception as e:
            print(str(e))
            continue






if __name__ == '__main__':
    main()