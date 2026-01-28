from global_functions import read_file


def get_whitelist_users():
    users = read_file("whitelist.txt")
    return users


def add_new_user(user_name):
    ...

