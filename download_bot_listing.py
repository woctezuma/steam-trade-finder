# Objective: automatically download the list of userIDs of ASF bots.

import json

import requests
from bs4 import BeautifulSoup

from utils import get_bot_listing_file_name


def get_bot_listing_url():
    bot_listing_url = 'https://asf.justarchi.net/STM'

    return bot_listing_url


def get_stm_url_prefix():
    stm_url_prefix = 'https://www.steamtradematcher.com/tools/specscan/'

    return stm_url_prefix


def get_steam_trade_offer_url_prefix():
    steam_trade_offer_url_prefix = 'https://steamcommunity.com/tradeoffer/new'

    return steam_trade_offer_url_prefix


def get_trade_parameter_separator():
    trade_parameter_separator = '&'
    return trade_parameter_separator


def get_trade_partner_prefix():
    trade_partner_prefix = '?partner='
    return trade_partner_prefix


def get_trade_token_prefix():
    trade_token_prefix = 'token='

    return trade_token_prefix


def get_trade_offer_url(partner, token):
    partner_info = get_trade_partner_prefix() + str(partner)
    token_info = get_trade_token_prefix() + str(token)

    trade_offer_url = (
        get_steam_trade_offer_url_prefix()
        + partner_info
        + get_trade_parameter_separator()
        + token_info
    )

    return trade_offer_url


def remove_prefix_from_str(input_str, prefix):
    if input_str.startswith(prefix):
        url_without_prefix = input_str[len(prefix) :]
    else:
        url_without_prefix = input_str

    return url_without_prefix


def download_bot_listing_as_html(bot_listing_url=None):
    if bot_listing_url is None:
        bot_listing_url = get_bot_listing_url()

    response = requests.get(url=bot_listing_url)

    html_doc = response.text

    return html_doc


def parse_bot_listing(html_doc, stm_url_prefix=None, steam_trade_offer_url_prefix=None):
    if stm_url_prefix is None:
        stm_url_prefix = get_stm_url_prefix()

    if steam_trade_offer_url_prefix is None:
        steam_trade_offer_url_prefix = get_steam_trade_offer_url_prefix()

    soup = BeautifulSoup(html_doc, 'html.parser')

    latest_trade_offer = None
    trade_offers = dict()

    for link in soup.find_all('a'):
        target_url = link.get('href')

        # Caveat: the order of the following if-statements matters!

        # First, the URL with the trade token:

        if target_url.startswith(steam_trade_offer_url_prefix):
            url_without_prefix = remove_prefix_from_str(
                target_url,
                steam_trade_offer_url_prefix,
            )
            steam_trade_offer_params = url_without_prefix.split(
                get_trade_parameter_separator(),
            )

            latest_trade_offer = dict()
            latest_trade_offer['partner'] = remove_prefix_from_str(
                steam_trade_offer_params[0],
                get_trade_partner_prefix(),
            )
            latest_trade_offer['token'] = remove_prefix_from_str(
                steam_trade_offer_params[1],
                get_trade_token_prefix(),
            )

        # Second, the URL with the scan by StreamTradeMatcher:

        if target_url.startswith(stm_url_prefix):
            user_id_as_str = remove_prefix_from_str(target_url, stm_url_prefix)

            user_id = int(user_id_as_str)

            trade_offers[user_id] = dict()
            trade_offers[user_id]['partner'] = latest_trade_offer['partner']
            trade_offers[user_id]['token'] = latest_trade_offer['token']

    return trade_offers


def download_and_parse_bot_listing(
    bot_listing_url=None,
    stm_url_prefix=None,
    steam_trade_offer_url_prefix=None,
    bot_listing_file_name=None,
    save_to_disk=True,
):
    if bot_listing_url is None:
        bot_listing_url = get_bot_listing_url()

    if stm_url_prefix is None:
        stm_url_prefix = get_stm_url_prefix()

    if steam_trade_offer_url_prefix is None:
        steam_trade_offer_url_prefix = get_steam_trade_offer_url_prefix()

    if bot_listing_file_name is None:
        bot_listing_file_name = get_bot_listing_file_name()

    html_doc = download_bot_listing_as_html(bot_listing_url=bot_listing_url)

    latest_trade_offers = parse_bot_listing(
        html_doc,
        stm_url_prefix=stm_url_prefix,
        steam_trade_offer_url_prefix=steam_trade_offer_url_prefix,
    )

    if save_to_disk:
        update_and_save_bot_listing_to_disk(
            latest_trade_offers,
            bot_listing_file_name=bot_listing_file_name,
        )

    return latest_trade_offers


def load_bot_listing_from_disk(bot_listing_file_name=None):
    if bot_listing_file_name is None:
        bot_listing_file_name = get_bot_listing_file_name()

    with open(bot_listing_file_name, 'r') as f:
        original_trade_offers = json.load(f)

    return original_trade_offers


def save_bot_listing_to_disk(trade_offers, bot_listing_file_name=None):
    if bot_listing_file_name is None:
        bot_listing_file_name = get_bot_listing_file_name()

    with open(bot_listing_file_name, 'w') as f:
        json.dump(trade_offers, f)

    return


def overwrite_trade_offers(original_trade_offers, latest_trade_offers):
    aggregated_trade_offers = original_trade_offers
    for user_id in latest_trade_offers:
        aggregated_trade_offers[user_id] = latest_trade_offers[user_id]

    return aggregated_trade_offers


def update_and_save_bot_listing_to_disk(
    latest_trade_offers,
    bot_listing_file_name=None,
):
    if bot_listing_file_name is None:
        bot_listing_file_name = get_bot_listing_file_name()

    original_trade_offers = load_bot_listing_from_disk(
        bot_listing_file_name=bot_listing_file_name,
    )

    aggregated_trade_offers = overwrite_trade_offers(
        original_trade_offers,
        latest_trade_offers,
    )

    save_bot_listing_to_disk(
        aggregated_trade_offers,
        bot_listing_file_name=bot_listing_file_name,
    )

    return


def main():
    latest_trade_offers = download_and_parse_bot_listing()

    return True


if __name__ == '__main__':
    main()
