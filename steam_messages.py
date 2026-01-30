from steam_extraction import *


def get_message_cases():

    if check_file("cs_market_data/output_files/output_prices_cases.txt"):
        responses = fetch_data(read_file("cs_market_data/input_files/cases.txt"))
        print(responses)
        save_data_to_file("cs_market_data/output_files/output_prices_cases.txt", responses)
    else:
        responses = get_data_from_file("cs_market_data/output_files/output_prices_cases.txt")
        print(responses)

    message = "    SKRZYNKI CS2    \n"
    print(responses[0])
    message += str(datetime.fromtimestamp(responses[0]))[:-7] + "\n"

    for i in responses[1:]:
        message += f"{i[0].replace("%20","").replace("%26","")[:-4]}\n Aktualna: {i[1]} Mediana: {i[2]}\n\n"
    return message


def get_message_stockholm_capsules():
    if check_file("cs_market_data/output_files/output_prices_capsules_stockholm.txt"):
        responses = fetch_data(read_file("cs_market_data/input_files/stockholm_capsules.txt"))
        print(responses)
        save_data_to_file("cs_market_data/output_files/output_prices_capsules_stockholm.txt", responses)
    else:
        responses = get_data_from_file("cs_market_data/output_files/output_prices_capsules_stockholm.txt")
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