import requests, time, json, datetime, os, random, logging
import argparse, sys
from santa_shares import Shop, User

logging.basicConfig(level=logging.DEBUG)

API_URL = os.environ.get("SANTA_API_URL", "https://santa-shares.azurewebsites.net")

class ManualBot:

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("command")
        args = parser.parse_args(sys.argv[1:2])
        command_name = args.command

        if hasattr(self, command_name):
            command = getattr(self, command_name)
            command()

    def buy(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("user_name")
        parser.add_argument("item_id")
        parser.add_argument("amount", default=1)
        args = parser.parse_args(sys.argv[2:])

        current_user_name = os.environ.get("SANTA_CURRENT_USER", None)
        if current_user_name is None:
            print("Need to register a user first.")
            return
        
        user_name = args.user_name
        item_id = args.item_id
        amount = args.amount

        user = User(API_URL, user_name)
        user.register()
        user.buy(item_id, amount)

    def sell(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("user_name")
        parser.add_argument("item_id")
        parser.add_argument("amount", default=1)
        args = parser.parse_args(sys.argv[2:])

        current_user_name = os.environ.get("SANTA_CURRENT_USER", None)
        if current_user_name is None:
            print("Need to register a user first.")
            return
        
        user_name = args.user_name
        item_id = args.item_id
        amount = args.amount

        user = User(API_URL, user_name)
        user.register()
        user.sell(item_id, amount)

if __name__ == "__main__":
    ManualBot()