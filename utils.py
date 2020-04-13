# The code shown below is an excerpt from:
#   https://github.com/woctezuma/steam-market/blob/master/utils.py


import datetime
import json
from pathlib import Path


def get_data_folder():
    data_folder = 'data/'
    Path(data_folder).mkdir(exist_ok=True)

    return data_folder


def get_bot_listing_file_name():
    bot_listing_file_name = get_data_folder() + 'asf_bots.json'

    return bot_listing_file_name


def get_temp_base_file_name_suffixe():
    temp_file_name = 'temp.json'

    return temp_file_name


def get_temp_base_file_name():
    temp_base_file_name = '{}_{}'.format(
        get_current_day_as_str(),
        get_temp_base_file_name_suffixe(),
    )

    return temp_base_file_name


def get_current_day_as_str():
    current_day_as_str = datetime.date.today().isoformat()

    return current_day_as_str


def save_to_disk(data,
                 base_file_name=None):
    if base_file_name is None:
        base_file_name = get_temp_base_file_name()

    output_file_name = get_data_folder() + base_file_name

    with open(output_file_name, 'w') as f:
        json.dump(data, f)

    return


def load_from_disk(base_file_name=None):
    if base_file_name is None:
        base_file_name = get_temp_base_file_name()

    input_file_name = get_data_folder() + base_file_name

    with open(input_file_name, 'r') as f:
        data = json.load(f)

    return data


def main():
    return True


if __name__ == '__main__':
    main()
