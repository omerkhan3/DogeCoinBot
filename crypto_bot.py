#!/usr/bin/env python3
import requests
import json
import time
import hmac
from hashlib import md5
from bittrex.bittrex import *
import pprint
#import pandas as pd
import csv

def read_last_line(fname):
    with open(fname) as file:
        for line in (file.readlines() [-1:]):
            line_split=line.split(',')
            return(line_split)


csv_file = 'YOUR_PATH_HERE/order_log.csv'
class Bittrex_Bot:
    def __init__(self, ticker):
        #self.account_info = get_account_info()
        self.bittrex_v2 = Bittrex(api_key, api_secret, api_version=API_V2_0)
        self.bittrex_v1 = Bittrex(api_key, api_secret, api_version=API_V1_1)
        self.usd_available_balance = self.get_available_balance(ticker.split('-')[0])
        self.doge_available_balance = self.get_available_balance(ticker.split('-')[1])
        self.ticker_for_bot = ticker
        self.ticker_price = self.get_price()
        self.last_order = read_last_line(csv_file)
        #self.order_log = pd.read_csv('order_log.csv')

    def get_markets(self):
        response = self.bittrex_v1.get_markets()
        if response['success'] == True:
            print(response)


    def get_available_balance(self, symbol):
        response = self.bittrex_v2.get_balance(symbol)
        try:
            if response['success'] == True:
                return(response['result']['Available'])
            else:
                return 0
        except TypeError:
            return 0


    def get_price(self):
        response = self.bittrex_v1.get_ticker(self.ticker_for_bot)
        if response['success'] == True:
            return(response['result']['Ask'])

    def price_action(self):
        current_ticker_price = self.get_price()
        last_order_price = float(self.last_order[1])
        last_order_direction = self.last_order[3].strip()
        file_object = open('YOUR_PATH_HERE/output.txt', 'a')
        file_object.write("\n current price: " + str(current_ticker_price) + ", last price: " + str(last_order_price) + ", " + last_order_direction)
        file_object.close()
        if last_order_direction == "BUY":
            if (current_ticker_price - last_order_price) >= (0.01 * last_order_price) :
                self.make_sell(doge_available_balance)
        elif last_order_direction == "SELL":
            print(last_order_price, current_ticker_price)
            if (last_order_price - current_ticker_price) >= (0.01 * last_order_price) :
                self.make_buy((self.usd_available_balance - (0.004 * self.usd_available_balance))/self.ticker_price)

    def write_to_order_book(self, file_name, list_of_elem):
        with open(csv_file, 'a+', newline='') as write_obj:
            csv_writer = csv.writer(write_obj)
            csv_writer.writerow(list_of_elem)

    def print_account_info(self):
        print("USD Balance: " + str(self.usd_available_balance))
        print("DOGE Balance: " + str(self.doge_available_balance))
        print("Ticker For Bot: " + self.ticker_for_bot)

    def make_buy(self, quantity):
        response = self.bittrex_v1.buy_limit(market=self.ticker_price, quantity=quantity, rate=self.ticker_price)
        if response['success'] == True:
            uuid = response['result']['uuid']
            self.write_to_order_book(csv_file, [uuid, self.ticker_price, quantity, "BUY"])
            print("BUY ORDER COMPLETED")

    def make_sell(self, quantity):
        response = self.bittrex_v1.sell_limit(market=self.ticker_price, quantity=quantity, rate=self.ticker_price)
        if response['success'] == True:
            uuid = response['result']['uuid']
            self.write_to_order_book(csv_file, [uuid, self.ticker_price, quantity, "SELL"])
            print("SELL ORDER COMPLETED")

bittrex_bot = Bittrex_Bot('USD-DOGE')
bittrex_bot.price_action()
