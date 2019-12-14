import requests, time, json, datetime, os, random
import argparse, sys
from santa_shares import Shop, User


class Bot(object):
    """ This class defines the bot, and handles the API"""
    def __init__(self):
        API_URL = "https://santa-shares.azurewebsites.net"
        self.shop = Shop(API_URL)
        self.user = User(API_URL, "happy-stoic")
        self.user.register()
        time.sleep(1)

    def print_balance(self):
        status = self.user.get_status()
        print(f"I've got [£{status['balance'] / 100:.2f}] cash left.")
        return status['balance']

    def get_items(self):
        return self.shop.get_items()


class BotPlotter(object):
    """Generates plots showing the history and current status of the market, and what the bot has done."""
    pass


if __name__ == '__main__':
    blitzen = Bot()
    blitzen.print_balance()
