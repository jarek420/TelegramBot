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
    # if file_timestamp == '':
    #     file_timestamp = 123
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


def get_message_cases():

    if check_file("TelegramBot/output_prices_cases.txt"):
        responses = fetch_data(read_file("TelegramBot/cases.txt"))
        print(responses)
        save_data_to_file("TelegramBot/output_prices_cases.txt", responses)
    else:
        responses = get_data_from_file("TelegramBot/output_prices_cases.txt")
        print(responses)

    message = "    SKRZYNKI CS2    \n"
    print(responses[0])
    message += str(datetime.fromtimestamp(responses[0]))[:-7] + "\n"

    for i in responses[1:]:
        message += f"{i[0].replace("%20","").replace("%26","")[:-4]}\n Aktualna: {i[1]} Mediana: {i[2]}\n\n"
    return message


def get_message_stockholm_capsules():
    if check_file("TelegramBotoutput_prices_capsules_stockholm.txt"):
        responses = fetch_data(read_file("TelegramBot/stockholm_capsules.txt"))
        print(responses)
        save_data_to_file("TelegramBot/output_prices_capsules_stockholm.txt", responses)
    else:
        responses = get_data_from_file("TelegramBot/output_prices_capsules_stockholm.txt")
        print(responses)

    message = "Kapsuły CS2    \n"
    print(responses[0])
    message += str(datetime.fromtimestamp(responses[0]))[:-7] + "\n"

    for i in responses[1:]:
        name = (
            i[0].replace("%20","")
            .replace("%26","")
            .replace("Stockholm","")
            .replace("Sticker","")
            .replace("Cap","")
        )[:-4]
        message += f"{name}\n Aktualna: {i[1]} Mediana: {i[2]}\n\n"
    return message
# get_message_stockholm_capsules()