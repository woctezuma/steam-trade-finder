import json

from inventory_utils import get_my_steam_profile_id, get_steam_inventory_file_name
from inventory_utils import load_steam_inventory, download_steam_inventory
from utils import get_data_folder


def check_whether_items_for_given_app_exist_in_inventory_of_given_user(market_app_id,
                                                                       profile_id=None,
                                                                       update_steam_inventory=False,
                                                                       verbose=True):
    if profile_id is None:
        profile_id = get_my_steam_profile_id()

    steam_inventory = load_steam_inventory(profile_id=profile_id,
                                           update_steam_inventory=update_steam_inventory)

    total_inventory_count = steam_inventory['total_inventory_count']

    try:
        last_asset_id = steam_inventory['last_assetid']
    except KeyError:
        last_asset_id = None

    while last_asset_id is not None:
        print('Downloading additional data for userID {} (total inventory count= {}) starting from assetID {}.'.format(
            profile_id,
            total_inventory_count,
            last_asset_id,
        ))

        if total_inventory_count > 50000:
            break

        steam_inventory_update = download_steam_inventory(profile_id=profile_id,
                                                          save_to_disk=False,
                                                          start_asset_id=last_asset_id)
        try:
            last_asset_id = steam_inventory_update['last_assetid']
        except KeyError:
            last_asset_id = None

        steam_inventory['assets'] += steam_inventory_update['assets']
        steam_inventory['descriptions'] += steam_inventory_update['descriptions']

        if last_asset_id is None:
            del steam_inventory['more_items']
            del steam_inventory['last_assetid']
        else:
            steam_inventory['more_items'] = steam_inventory_update['more_items']
            steam_inventory['last_assetid'] = steam_inventory_update['last_assetid']

        with open(get_steam_inventory_file_name(profile_id), 'w') as f:
            json.dump(steam_inventory, f)

    try:
        descriptions = steam_inventory['rgDescriptions']  # Warning: this is a dictionary.
        if verbose:
            print('Inventory downloaded from the *old* end-point: {}'.format(profile_id))
    except KeyError:
        descriptions = steam_inventory['descriptions']  # Warning: this is a list.
        if verbose:
            print('Inventory downloaded from the *new* end-point: {}'.format(profile_id))
    except TypeError:
        descriptions = dict()

    market_app_has_been_found = False

    for element in descriptions:
        try:
            market_fee_app = descriptions[element]['market_fee_app']
        except TypeError:
            market_fee_app = element['market_fee_app']

        if str(market_fee_app) == str(market_app_id):
            market_app_has_been_found = True
            break

    if verbose and market_app_has_been_found:
        print('Items related to appID={} found in inventory of userID={}'.format(market_app_id, profile_id))

    return market_app_has_been_found


def check_all_asf_bots(market_app_id):
    with open(get_data_folder() + 'asf_bots.txt', 'r') as f:
        lines = f.readlines()

    for profile_id_as_str in lines:
        profile_id = int(profile_id_as_str.strip())

        steam_inventory_file_name = get_steam_inventory_file_name(profile_id)

        market_app_has_been_found = check_whether_items_for_given_app_exist_in_inventory_of_given_user(
            market_app_id=market_app_id,
            profile_id=profile_id)

    return


def main(self_test=False):
    market_app_id = 448720

    if self_test:
        market_app_has_been_found = check_whether_items_for_given_app_exist_in_inventory_of_given_user(
            market_app_id=market_app_id,
            profile_id=None)
    else:
        check_all_asf_bots(market_app_id)

    return True


if __name__ == '__main__':
    main()
