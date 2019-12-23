"""
Implements the functions necessary to access every queue
function without actually needing a visual interface.
"""


import os
import sys
import json
import requests
import dotenv


def index(link):
    """Wakes up the server by asking for its root page."""
    return requests.get(f'{link}/')


def get_next(link):
    """Gets a number."""
    payload = {
        "key": os.getenv("KEY")
    }
    return requests.get(f'{link}/number', json=payload).json()


def check_number(link, number, plain_key):
    """Checks if number and plain key match."""
    payload = {
        "key": os.getenv("KEY"),
        "plain_key": plain_key
    }
    return requests.post(f'{link}/number/{number}', json=payload).json()


if __name__ == "__main__":
    LINK = "http://127.0.0.1:5000"
    COMMANDS = {
        "index":        index,
        "get_next":     get_next,
        "check_number": check_number
    }

    dotenv.load_dotenv()
    try:
        RESPONSE = COMMANDS[sys.argv[1]](LINK, *sys.argv[2:])
    except IndexError:
        if len(sys.argv) <= 1:
            print("\n\n\n\tInvalid script call. To use the script, run:")
            print("\tpython3 ghost_client.py command *args")
            print("\tWhere *args are the arguments separated by space and "
                  "command corresponds to one of the following:")
            print(f'\t\t{", ".join(COMMANDS.keys())}\n\n')
            sys.exit(1)
    try:
        print(json.dumps(RESPONSE, indent=2, sort_keys=False))
    except TypeError:
        print(RESPONSE.text)
