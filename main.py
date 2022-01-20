import json
import random
import time

import requests

cfg_path = "cfg.json"
accounts_path = "accounts.json"


def load_data(path):
    with open(path, "r") as f:
        return json.load(f)


def get_token(client_id, client_secret):
    data = {
        'captcha_key': None,
        'gift_code_sku_id': None,
        'login': client_id,
        'login_source': None,
        'password': client_secret,
        'undelete': False
    }
    headers = {
        'Content-Type': 'application/json',
        'Referer': 'https://discord.com/login',
        'Host': 'discord.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15'
    }
    j = json.dumps(data)
    r = requests.post(url='https://discord.com/api/v9/auth/login',
                      data=j,
                      headers=headers)
    r.raise_for_status()
    return r.json()


def get_guild_information(channel_id):
    url = cfg["invite_url"] % channel_id
    r = requests.get(url)
    return r.json()


def get_invite_enter(token, channel_id) -> requests.Response:
    url = cfg["invite_url"] % channel_id
    headers = {
        'Content-Type': 'application/json',
        'Referer': url,
        'Host': 'discord.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
        'Authorization': token
    }
    r = requests.post(url,
                      data=json.dumps({}),
                      headers=headers)
    return r.json()


def get_TermAndConditions(token, channel_id):
    url = cfg["get_term_conditions_url"] % channel_id
    headers = {
        'Content-Type': 'application/json',
        'Referer': url,
        'Host': 'discord.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
        'Authorization': token
    }
    r = requests.get(url, headers=headers)
    return r.json()


def accept_TermAndConditions(token, channel_id, data):
    url = cfg["term_conditions_url"] % channel_id
    data["form_fields"][0]["response"] = True
    del data["description"]
    headers = {
        'Content-Type': 'application/json',
        # 'Referer': url,
        'Host': 'discord.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
        'Authorization': token
    }
    r = requests.put(url,
                     data=json.dumps(data),
                     headers=headers)
    return r.json()


def add_reaction(url, token):
    # url = credentials["invite_url"] % channel_id
    headers = {
        'Content-Type': 'application/json',
        'Host': 'discord.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
        'Authorization': token
    }
    r = requests.put(url,
                     data=json.dumps({}),
                     headers=headers)


if __name__ == "__main__":

    cfg = load_data(cfg_path)
    accounts = load_data(accounts_path)
    API_ENDPOINT = 'https://discord.com'

    print("#### THE PROGRAM IS STARTING ... ###")
    print("\nNumber of available accounts is " + str(len(accounts["accounts"])))

    counter = 1
    channel_code = cfg["invite_link"].split("/")[-1]

    message_to_be_reacted = cfg["message_link"]
    emoji_link = cfg["emoji_link"]

    upper_limit = min(len(accounts["accounts"]), cfg["max_account"]) if cfg["max_account"] != -1 else len(
        accounts["accounts"])

    print(f"The program will start with {upper_limit} accounts")
    time.sleep(1)
    success = 0
    for i in range(upper_limit):
        email = accounts["accounts"][i]["email"]
        password = email = accounts["accounts"][i]["password"]

        print(f"Account No: {counter} started.")

        auth_info = get_token(email, password)
        token = auth_info["token"]
        print(f"The token is retrieved: {token}")

        invitation_result = get_invite_enter(token, channel_code)
        if invitation_result.status_code == 200:
            print(f"The account no {counter} has successfully accepted the invitation.")
            success += 1
        else:
            print(f"The account no {counter} has failed to accept the invitation. -> ", invitation_result)
            continue

        channel_id = invitation_result["guild"]["id"]
        print("Guild Name: " + invitation_result["guild"]["name"])

        if cfg["requests"]["term_and_conditions"]:
            term_and_conditions = get_TermAndConditions(token, channel_id)
        if cfg["requests"]["reaction"]:
            reaction = add_reaction(emoji_link, token)
        counter += 1

        s_time = random.randint(1, 4)
        print(f"The program will sleep {s_time} seconds")
        time.sleep(s_time)

    print(f"Number of bots that accepts invitation is {success} among {upper_limit}")
    print("### THE PROGRAM HAS FINISHED ### ")
    input()
