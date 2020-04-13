from data_utils import get_hard_coded_market_dict
from download_bot_listing import load_bot_listing_from_disk, get_bot_listing_url, get_trade_offer_url


def get_steam_card_exchange_url(app_id):
    steam_card_exchange_url = 'https://www.steamcardexchange.net/index.php?gamepage-appid-{}'.format(app_id)

    return steam_card_exchange_url


def get_profile_url(profile_id):
    profile_url = 'https://steamcommunity.com/profiles/' + str(profile_id) + '/inventory/#753'
    return profile_url


def display_results_with_markdown(results,
                                  hard_coded_market_dict=None,
                                  trade_offers=None):
    if hard_coded_market_dict is None:
        hard_coded_market_dict = get_hard_coded_market_dict()

    if trade_offers is None:
        trade_offers = load_bot_listing_from_disk()

    bot_listing_url = get_bot_listing_url()
    print(bot_listing_url)

    for market_app_id in results:
        app_name = hard_coded_market_dict[str(market_app_id)]
        steam_card_exchange_url = get_steam_card_exchange_url(market_app_id)

        header = '# [{}]({})'.format(
            app_name,
            steam_card_exchange_url,
        )
        print(header)

        for profile_id in results[market_app_id]:
            profile_trade_offer = trade_offers[str(profile_id)]

            steam_community_url = get_profile_url(profile_id)
            trade_offer_url = get_trade_offer_url(partner=profile_trade_offer['partner'],
                                                  token=profile_trade_offer['token'])

            line = '1.   [userID={}]({}) [offer]({})'.format(
                profile_id,
                steam_community_url,
                trade_offer_url,
            )
            print(line)

    return


def main():
    results = {
        '270010': [76561197973009892],
        '318090': [76561197973009892, 76561198160392629],
    }

    display_results_with_markdown(results)

    return True


if __name__ == '__main__':
    main()
