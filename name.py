import requests
import json
import time
import schedule
from datetime import datetime, timedelta

def change_name():
    with open('config.json') as config_file:
        config = json.load(config_file)
        access_token = config['access_token']
        new_name = config['new_name']
        max_retries = config.get('max_retries', 100)

    SUCCESS = 200
    RATE_LIMIT = 429
    TAKEN = 403

    endpoint = f"https://api.minecraftservices.com/minecraft/profile/name/{new_name}"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    for attempt in range(max_retries):
        response = requests.put(endpoint, headers=headers)

        # Check the response status
        if response.status_code == SUCCESS:
            print(" > Congrats, name sniped!")
            break
        elif response.status_code == RATE_LIMIT:
            print(" > Rate limit exceeded. Waiting before retrying.")
            time.sleep(1)
        elif response.status_code == TAKEN:
            print(" > Username is already taken.")
        else:
            print(f"Error: {response.status_code} - {response.text}")

        time.sleep(1)
    else:
        print(" > Unable to change the name :(")

with open('config.json') as config_file:
    config = json.load(config_file)
    scheduled_time_str = config.get('scheduled_time', '')
    scheduled_time = datetime.strptime(scheduled_time_str, '%H:%M:%S')

schedule.every().day.at(scheduled_time.strftime('%H:%M:%S')).do(change_name)

while True:
    schedule.run_pending()
    time.sleep(1)
