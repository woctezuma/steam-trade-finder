from data_utils import get_hard_coded_market_dict, get_my_profile_id
from download_bot_listing import load_bot_listing_from_disk, get_bot_listing_url, get_trade_offer_url
from utils import load_from_disk


def get_steam_card_exchange_url(app_id):
    steam_card_exchange_url = 'https://www.steamcardexchange.net/index.php?gamepage-appid-{}'.format(app_id)

    return steam_card_exchange_url


def get_profile_url(profile_id):
    profile_url = 'https://steamcommunity.com/profiles/' + str(profile_id) + '/inventory/#753'
    return profile_url


def get_user_markdown(profile_id):
    steam_community_url = get_profile_url(profile_id)

    user_markdown = '[userID={}]({})'.format(
        profile_id,
        steam_community_url,
    )

    return user_markdown


def get_offer_markdown(profile_id,
                       trade_offers=None):
    if trade_offers is None:
        trade_offers = load_bot_listing_from_disk()

    profile_trade_offer = trade_offers[str(profile_id)]

    partner = profile_trade_offer['partner']
    token = profile_trade_offer['token']

    if partner is not None and token is not None:
        trade_offer_url = get_trade_offer_url(partner=partner,
                                              token=token)

        offer_markdown = '[offer]({})'.format(
            trade_offer_url,
        )
    else:
        offer_markdown = ''

    return offer_markdown


def display_results_with_markdown(results,
                                  hard_coded_market_dict=None,
                                  blacklisted_profile_ids=None,
                                  trade_offers=None):
    if hard_coded_market_dict is None:
        hard_coded_market_dict = get_hard_coded_market_dict()

    if trade_offers is None:
        trade_offers = load_bot_listing_from_disk()

    if blacklisted_profile_ids is None:
        blacklisted_profile_ids = []

    # Blacklist my own profile id, because I cannot trade with myself:
    my_profile_id = get_my_profile_id()
    my_profile_id_as_str = str(my_profile_id)
    blacklisted_profile_ids.append(my_profile_id_as_str)
    print('Black-listed profiles: {}'.format(
        blacklisted_profile_ids)
    )

    bot_listing_url = get_bot_listing_url()
    print(bot_listing_url)

    app_ids_sorted_by_app_name = sorted(results,
                                        key=lambda x: hard_coded_market_dict[str(x)])

    for market_app_id in app_ids_sorted_by_app_name:
        app_name = hard_coded_market_dict[str(market_app_id)]
        steam_card_exchange_url = get_steam_card_exchange_url(market_app_id)

        header = '# [{}]({})'.format(
            app_name,
            steam_card_exchange_url,
        )
        print(header)

        sorted_profile_ids = sorted(results[market_app_id],
                                    key=lambda x: int(x))

        for profile_id in sorted_profile_ids:
            if str(profile_id) in blacklisted_profile_ids:
                continue

            user_markdown = get_user_markdown(profile_id)
            offer_markdown = get_offer_markdown(profile_id,
                                                trade_offers=trade_offers)

            line = '1.   {} {}'.format(
                user_markdown,
                offer_markdown,
            )
            print(line)

    return


def main():
    try:
        results = load_from_disk()
    except FileNotFoundError:
        print('File not found for current date. Displaying dummy results.')

        results = {
            '270010': [76561197973009892],
            '318090': [76561197973009892, 76561198160392629],
        }

    display_results_with_markdown(results)

    return True


if __name__ == '__main__':
    main()
