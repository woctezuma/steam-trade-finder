# The code shown below is an excerpt from:
#   https://github.com/woctezuma/steam-market/blob/master/inventory_utils.py

import json

import requests

from personal_info import get_cookie_dict, update_and_save_cookie_to_disk_if_values_changed
from utils import get_data_folder


def get_my_steam_profile_id():
    my_profile_id = '76561198028705366'

    return my_profile_id


def get_steam_inventory_url(profile_id=None, app_id=753, context_id=6):
    if profile_id is None:
        profile_id = get_my_steam_profile_id()

    # References:
    # https://github.com/Alex7Kom/node-steam-tradeoffers/issues/114
    # https://dev.doctormckay.com/topic/332-identifying-steam-items/
    # steam_inventory_url = 'https://steamcommunity.com/profiles/'  + str(profile_id) + '/inventory/json/'

    # Reference for the new API end-point: https://steamcommunity.com/discussions/forum/1/1736595227843280036/
    steam_inventory_url = 'https://steamcommunity.com/inventory/' + str(profile_id) + '/'  # TODO
    steam_inventory_url += str(app_id) + '/' + str(context_id) + '/'

    return steam_inventory_url


def get_steam_inventory_file_name(profile_id):
    steam_inventory_file_name = get_data_folder() + 'inventory_' + str(profile_id) + '.json'

    return steam_inventory_file_name


def load_steam_inventory_from_disk(profile_id=None):
    if profile_id is None:
        profile_id = get_my_steam_profile_id()

    try:
        with open(get_steam_inventory_file_name(profile_id), 'r') as f:
            steam_inventory = json.load(f)
    except FileNotFoundError:
        steam_inventory = download_steam_inventory(profile_id, save_to_disk=True)

    return steam_inventory


def load_steam_inventory(profile_id=None, update_steam_inventory=False):
    if profile_id is None:
        profile_id = get_my_steam_profile_id()

    if update_steam_inventory:
        steam_inventory = download_steam_inventory(profile_id, save_to_disk=True)
    else:
        steam_inventory = load_steam_inventory_from_disk(profile_id=profile_id)

    return steam_inventory


def download_steam_inventory(profile_id=None,
                             save_to_disk=True,
                             start_asset_id=None):
    if profile_id is None:
        profile_id = get_my_steam_profile_id()

    cookie = get_cookie_dict()
    has_secured_cookie = bool(len(cookie) > 0)

    url = get_steam_inventory_url(profile_id=profile_id)

    req_data = dict(
        l='english',
        count=5000,
    )  # TODO

    if start_asset_id is not None:
        req_data['start_assetid'] = start_asset_id # TODO

    if has_secured_cookie:
        resp_data = requests.get(url,
                                 params=req_data,  # TODO
                                 cookies=cookie)
    else:
        resp_data = requests.get(url,
                                 params=req_data)  # TODO

    status_code = resp_data.status_code

    if status_code == 200:
        steam_inventory = resp_data.json()

        if has_secured_cookie:
            jar = dict(resp_data.cookies)
            cookie = update_and_save_cookie_to_disk_if_values_changed(cookie, jar)

        if save_to_disk:
            with open(get_steam_inventory_file_name(profile_id), 'w') as f:
                json.dump(steam_inventory, f)
    else:
        print('Inventory for profile {} could not be loaded. Status code {} was returned.'.format(profile_id,
                                                                                                  status_code))
        steam_inventory = None

    return steam_inventory


def get_session_id(cookie=None):
    if cookie is None:
        cookie = get_cookie_dict()

    session_id = cookie['sessionid']

    return session_id


def get_request_headers():
    # Reference: https://dev.doctormckay.com/topic/287-automatic-market-seller/

    request_headers = {
        'Origin': 'https://steamcommunity.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'https://steamcommunity.com/my/inventory/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3'
    }

    return request_headers


def main():
    steam_inventory = load_steam_inventory()
    return True


if __name__ == '__main__':
    main()
