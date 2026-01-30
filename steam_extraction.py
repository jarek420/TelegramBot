import requests
import time
from datetime import datetime
import ast
from global_functions import read_file

GREEN = "\033[32m"
RESET = "\033[0m"
RED = "\033[31m"


def steam_encode(name: str) -> str:
    return (
        name.replace("%", "%25")
            .replace(" ", "%20")
            .replace("&", "%26")
            .replace(":", "%3A")
            .replace("|", "%7C")
            .replace("'", "%27")
    )


def get_data_from_file(file_name):
    data = []

    with open(file_name, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            if line[0].isdigit():
                data.append(float(line))
            else:
                data.append(ast.literal_eval(line))

    return data


def check_file(file_name):
    with open(file_name, 'r', encoding = "utf-8") as f:
        file_timestamp = f.readline().strip()
    diff = float(time.time()) - float(file_timestamp)
    return diff >=3600


def save_data_to_file(file_name, data):
    with open(file_name, "w", encoding = "utf-8") as f:
        for line in data:
            f.write(str(line) + "\n")


def fetch_data(names):
    responses = []
    responses.append(time.time())
    counter = len(names)
    for i in names:
        name = steam_encode(i.strip())
        url = f"https://steamcommunity.com/market/priceoverview?appid=730&market_hash_name={name}&currency=6"
        res = requests.get(url).json()

        # ==== DEBUG ====
        if res['success'] == True:
            status = f"{GREEN}SUCCESS{RESET}"
        else:
            status = f"{RED}SUCCESS{RESET}"
    
        print(f"{GREEN}DEBUG{RESET}: Collecting{name}, {GREEN}STATUS: {status} {counter} items left")
        # ==== DEBUG ====

        responses.append([name, res['lowest_price'], res['median_price']])
        counter -= 1

    return responses


def get_item_price_by_name(name):
    # steps:
    # get all files from cs_market_data/input_files
    # find best matching name eg: user types "Stockholm 2021" -> program returns all capsules that have stockholm 2021 in name
    # eg2: user searches for dreams and nightmares / dream nightmares and it will leave him with proper output which is]: Dreams & Nightmares Case
    # main goal is to give uuser back best matching item so even if he misstype something it will return him an output.
    # then get thius name run fetch_data(names) and return responses
    ...



# get_message_stockholm_capsules()