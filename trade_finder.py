# Objective: find ASF users who own Steam community items (trading card, profile background, emoticon) of a given set,
#            which could potentially allow us to send them **neutral** Steam trades to complete a set.

import json

from download_bot_listing import load_bot_listing_from_disk, get_trade_offer_url
from inventory_utils import get_my_steam_profile_id, get_steam_inventory_file_name
from inventory_utils import load_steam_inventory, download_steam_inventory


def get_profile_url(profile_id):
    profile_url = 'https://steamcommunity.com/profiles/' + str(profile_id) + '/inventory/#753'
    return profile_url


def check_whether_items_for_given_app_exist_in_inventory_of_given_user(market_app_id,
                                                                       profile_id=None,
                                                                       profile_trade_offer=None,
                                                                       update_steam_inventory=False,
                                                                       max_inventory_size=None,
                                                                       verbose=True):
    if profile_id is None:
        profile_id = get_my_steam_profile_id()

    if profile_trade_offer is None:
        trade_offer_url = None
    else:
        trade_offer_url = get_trade_offer_url(partner=profile_trade_offer['partner'],
                                              token=profile_trade_offer['token'])

    steam_inventory = load_steam_inventory(profile_id=profile_id,
                                           update_steam_inventory=update_steam_inventory)

    try:
        total_inventory_count = steam_inventory['total_inventory_count']
    except TypeError:
        # Private inventory (error 403 Forbidden)
        total_inventory_count = -1

    try:
        last_asset_id = steam_inventory['last_assetid']
    except KeyError:
        # Small Inventory, i.e. fewer items than num_inventory_items_per_query (5000). Hence no need for a second query.
        last_asset_id = None
    except TypeError:
        # Private inventory (error 403 Forbidden)
        last_asset_id = None

    # Reference: https://steamcommunity.com/discussions/forum/1/1736595227843280036/
    num_inventory_items_per_query = 5000  # value corresponding to the new API end-point. Not chosen by the user!

    query_counter = 0

    while last_asset_id is not None:
        print('Downloading additional data for userID {} (total inventory count = {}) starting from assetID {}.'.format(
            profile_id,
            total_inventory_count,
            last_asset_id,
        ))

        if total_inventory_count < 0:
            print('Total inventory count unknown ({}). Exiting the query loop.'.format(
                total_inventory_count
            ))
            break

        if max_inventory_size is not None and (query_counter * num_inventory_items_per_query) >= max_inventory_size:
            print('Total inventory count is large ({}). Exiting the query loop after {} queries of {} items.'.format(
                total_inventory_count,
                query_counter,
                num_inventory_items_per_query
            ))
            break

        steam_inventory_update = download_steam_inventory(profile_id=profile_id,
                                                          save_to_disk=False,
                                                          start_asset_id=last_asset_id)

        query_counter += 1

        if steam_inventory_update is None:
            # Usually due to status code 500 ("Internal Server Error")
            break

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
        try:
            descriptions = steam_inventory['descriptions']  # Warning: this is a list.
            if verbose:
                print('Inventory downloaded from the *new* end-point: {}'.format(profile_id))
        except KeyError:
            descriptions = dict()
            if verbose:
                print('Inventory without the expected field for descriptions: {}'.format(profile_id))
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

    if market_app_has_been_found:
        print('Items related to appID={} found in inventory of userID={} ({}) ({})'.format(market_app_id,
                                                                                           profile_id,
                                                                                           get_profile_url(profile_id),
                                                                                           trade_offer_url))

    return market_app_has_been_found


def check_all_asf_bots(market_app_ids,
                       max_inventory_size=50000):
    trade_offers = load_bot_listing_from_disk()

    profile_ids = set([int(profile_id_as_str.strip())
                       for profile_id_as_str in trade_offers
                       if len(profile_id_as_str.strip()) > 0])

    verbose = bool(len(market_app_ids) == 1)

    for profile_id in sorted(profile_ids):
        steam_inventory_file_name = get_steam_inventory_file_name(profile_id)

        print('Checking inventory of userID={}'.format(profile_id))

        profile_trade_offer = trade_offers[str(profile_id)]

        for market_app_id in market_app_ids:
            market_app_has_been_found = check_whether_items_for_given_app_exist_in_inventory_of_given_user(
                market_app_id=market_app_id,
                profile_id=profile_id,
                profile_trade_offer=profile_trade_offer,
                max_inventory_size=max_inventory_size,
                verbose=verbose)

    return


def main(self_test=False,
         market_app_ids=None,
         max_inventory_size=None,
         profile_id=None):
    if market_app_ids is None:
        # App: "Puzzle Box"
        # Reference: https://www.steamcardexchange.net/index.php?gamepage-appid-448720
        market_app_ids = [448720]

    if self_test:
        for market_app_id in market_app_ids:
            market_app_has_been_found = check_whether_items_for_given_app_exist_in_inventory_of_given_user(
                market_app_id=market_app_id,
                profile_id=profile_id,
                max_inventory_size=max_inventory_size)
    else:
        check_all_asf_bots(market_app_ids,
                           max_inventory_size=max_inventory_size)

    return True


if __name__ == '__main__':
    main()
