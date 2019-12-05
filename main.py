import requests, time, json, datetime, os

#API_URL = "https://santa-shares.azurewebsites.net"
API_URL = "http://localhost"

print("Starting bot...")
if not os.path.exists("bot.json"):
    USER_NAME = f"tom_bot_{datetime.datetime.now()}"

    response = requests.post(API_URL+"/api/users", json={ "user_name" : USER_NAME })
    if response.status_code != 201:
        print(f"[{response.status_code}]")
        exit()
    else:
        json_response = response.json()
        USER_ID = json_response.get("user_id")
        TOKEN = json_response.get("token")
        with open("bot.json", "w") as file:
            json.dump({
                "user_id" : USER_ID,
                "user_name" : USER_NAME,
                "token" : TOKEN,
            }, file)

with open("bot.json", "r") as file:
    json_data = json.load(file)
    USER_ID = json_data["user_id"]
    USER_NAME = json_data["user_name"]
    TOKEN = json_data["token"]

HEADERS = { "Authorization" : f"token {TOKEN}" }
time.sleep(1)

print(f"[{USER_NAME}] [{TOKEN}]")
while True:
    print("Requesting status...")

    response = requests.post(API_URL+"/api/buy", headers=HEADERS, json={
        "item_id" : 1,
        "user_id" : 1
    })
    #response = requests.get(API_URL+"/api/users/"+USER_ID, headers=HEADERS)
    # json_response = response.json()

    # if response.status_code != 200 or json_response.get('error') is not None:
    #     print(f"[{response.status_code}] [{json_response.get('error')}]")
    #     exit()
    # else:
    #     print(f"Balance: [{json_response['balance']}")

    time.sleep(5)