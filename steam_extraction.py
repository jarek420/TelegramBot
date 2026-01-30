import os
import difflib
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

def get_item_price_by_name(query: str,
                           input_dir: str = "cs_market_data/input_files",
                           max_suggestions: int = 10,
                           cutoff: float = 0.52):
    q = (query or "").strip()
    if not q:
        return {"query": query, "matches": [], "prices": []}

    q_low = q.lower()

    all_items = []
    for root, _, files in os.walk(input_dir):
        for fn in files:
            if fn.lower().endswith(".txt"):
                path = os.path.join(root, fn)
                try:
                    for line in read_file(path):
                        s = line.strip()
                        if s:
                            all_items.append(s)
                except FileNotFoundError:
                    continue

    uniq_items, seen = [], set()
    for it in all_items:
        if it not in seen:
            seen.add(it)
            uniq_items.append(it)

    substring_matches = [it for it in uniq_items if q_low in it.lower()]

    fuzzy_matches = []
    if len(substring_matches) < max_suggestions:
        def key(s: str) -> str:
            return "".join(ch.lower() if ch.isalnum() or ch.isspace() else " " for ch in s).strip()

        keys = {it: key(it) for it in uniq_items}
        qk = key(q)

        candidates = difflib.get_close_matches(
            qk,
            list(keys.values()),
            n=max_suggestions * 3,
            cutoff=cutoff
        )

        for it, k in keys.items():
            if k in candidates:
                fuzzy_matches.append(it)

    matches, seen2 = [], set()
    for it in substring_matches + fuzzy_matches:
        if it not in seen2:
            seen2.add(it)
            matches.append(it)
        if len(matches) >= max_suggestions:
            break

    if not matches:
        return {"query": query, "matches": [], "prices": []}

    return fetch_data(matches)



print(get_item_price_by_name("dreams nightmares"))
# get_message_stockholm_capsules()