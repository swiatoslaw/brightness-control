import json
import re
from json import JSONDecodeError

_key = 'last_value'
_rgx = r'^([0-9]\s\s|[1-9][0-9]\s|100)$'


def save_value(value):
    with open('data.json', mode='w') as F:
        json.dump({_key: value}, F)


def get_last_value():
    try:
        with open('data.json') as F:
            value = json.load(F).get(_key)

            if value and not re.match(_rgx, value):
                raise re.error(None)

            return value

    except (FileNotFoundError, JSONDecodeError) as e:
        return None


if __name__ == '__main__':
    print(get_last_value())
