import requests, time, json, datetime, os, random
import argparse, sys

parser = argparse.ArgumentParser()
parser.add_argument("user_name")
args = parser.parse_args(sys.argv[1:])

API_URL = "https://santa-shares.azurewebsites.net"
#API_URL = "http://localhost"
USER_NAME = args.user_name

print(f"Starting bot targeting [{API_URL}]")
if not os.path.exists(USER_NAME+".json"):

    response = requests.post(API_URL+"/api/users", json={ "user_name" : USER_NAME })
    if response.status_code != 201:
        print(f"[{response.status_code}]")
        exit()
    else:
        json_response = response.json()
        USER_ID = json_response.get("user_id")
        TOKEN = json_response.get("token")
        with open(USER_NAME+".json", "w") as file:
            json.dump({
                "user_id" : USER_ID,
                "user_name" : USER_NAME,
                "token" : TOKEN,
            }, file)

with open(USER_NAME+".json", "r") as file:
    json_data = json.load(file)
    USER_ID = json_data["user_id"]
    USER_NAME = json_data["user_name"]
    TOKEN = json_data["token"]

HEADERS = { "Authorization" : f"token {TOKEN}" }
time.sleep(1)

print(f"[{USER_NAME}] [{TOKEN}]")
while True:

    status = requests.get(API_URL+"/api/users/"+str(USER_ID), headers=HEADERS).json()
    print(f"I've got [£{status['balance']/100:.2f}] cash left.")

    # randomly buy or sell
    if random.random() > 0.5: # buy
        print("I'm gonna buy something...")
        items = requests.get(API_URL+"/api/items").json()
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
        requests.post(API_URL+"/api/buy", headers=HEADERS, json={ "item_id" : item["item_id"], "amount" : purchase_amount })
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
        response = requests.post(API_URL+"/api/sell", headers=HEADERS, json={ "item_id" : user_item["item_id"], "amount" : sale_amount })

    time.sleep(120)