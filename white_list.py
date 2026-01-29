from global_functions import read_file


def get_whitelist_users():
    output = []
    users = read_file("whitelist.txt")
    for i in users:
        data = int(i)
        output.append(data)
    return output


def add_new_user(user_name):
    ...

