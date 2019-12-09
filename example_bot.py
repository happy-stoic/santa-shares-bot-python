import requests, time, json, datetime, os, random
import argparse, sys
from santa_shares import Shop, User

parser = argparse.ArgumentParser()
parser.add_argument("user_name")
args = parser.parse_args(sys.argv[1:])

API_URL = "https://santa-shares.azurewebsites.net"
#API_URL = "http://localhost"

shop = Shop(API_URL)
user = User(API_URL, args.user_name)
user.register()

time.sleep(1)

while True:
    status = user.get_status()
    print(f"I've got [£{status['balance']/100:.2f}] cash left.")

    # randomly buy or sell
    if random.random() > 0.25: # buy
        print("I'm gonna buy something...")
        items = shop.get_items()
        item = items[random.randint(0, len(items)-1)]
        print(f"Chosen to buy [{item['item_name']}]")

        if item["amount"] == 0:
            print("None of those for sale..")
            continue
        purchase_amount = random.randint(1, item["amount"])
        purchase_price = purchase_amount * item["price"]

        if purchase_price > status["balance"]:
            print("Not enough cash for purchase.")
            continue

        print(f"Buying [{purchase_amount}] of [{item['item_name']}] for [£{purchase_price/100:.2f}]")
        user.buy(item["item_id"], purchase_amount)
    else:
        print("Hmmm what could I sell...")
        if len(status["items"]) == 0:
            print("Oh yeah I've got nothing to sell :(")
            continue

        user_item = status["items"][random.randint(0, len(status["items"])-1)]
        print(f"Let's get rid of some of these! [{user_item['item_name']}]")

        sale_amount =  random.randint(1, user_item["amount"])
        sale_price = sale_amount * (user_item['price'] - 100) # transaction fee
        if sale_price < 0:
            print("Ah there's no point selling them due to the transaction fee.")
            continue

        print(f"Selling [{sale_amount}] of [{user_item['item_name']}] for [£{sale_price/100:.2f}]")
        user.sell(user_item["item_id"], sale_amount)

    time.sleep(5)