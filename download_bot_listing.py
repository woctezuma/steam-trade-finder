import requests
from bs4 import BeautifulSoup

from utils import get_bot_listing_file_name


def get_bot_listing_url():
    bot_listing_url = 'https://asf.justarchi.net/STM'

    return bot_listing_url


def get_stm_url_prefix():
    stm_url_prefix = 'https://www.steamtradematcher.com/tools/specscan/'

    return stm_url_prefix


def download_bot_listing_as_html(bot_listing_url=None):
    if bot_listing_url is None:
        bot_listing_url = get_bot_listing_url()

    response = requests.get(url=bot_listing_url)

    html_doc = response.text

    return html_doc


def parse_bot_listing(html_doc,
                      stm_url_prefix=None):
    if stm_url_prefix is None:
        stm_url_prefix = get_stm_url_prefix()

    soup = BeautifulSoup(html_doc, 'html.parser')

    user_ids = set()

    for link in soup.find_all('a'):
        target_url = link.get('href')

        if stm_url_prefix in target_url:
            user_id_as_str = target_url.strip(stm_url_prefix)

            user_id = int(user_id_as_str)

            user_ids.add(user_id)

    return user_ids


def download_and_parse_bot_listing(bot_listing_url=None,
                                   stm_url_prefix=None,
                                   bot_listing_file_name=None,
                                   save_to_disk=True):
    if bot_listing_url is None:
        bot_listing_url = get_bot_listing_url()

    if stm_url_prefix is None:
        stm_url_prefix = get_stm_url_prefix()

    if bot_listing_file_name is None:
        bot_listing_file_name = get_bot_listing_file_name()

    html_doc = download_bot_listing_as_html(bot_listing_url=bot_listing_url)

    user_ids = parse_bot_listing(html_doc,
                                 stm_url_prefix=stm_url_prefix)

    if save_to_disk:
        update_and_save_bot_listing_to_disk(user_ids,
                                            bot_listing_file_name=bot_listing_file_name)

    return user_ids


def load_bot_listing_from_disk(bot_listing_file_name=None):
    if bot_listing_file_name is None:
        bot_listing_file_name = get_bot_listing_file_name()

    with open(bot_listing_file_name, 'r') as f:
        lines = f.readlines()

    user_ids = set()

    for user_id_as_str in lines:
        user_id = int(user_id_as_str.strip())

        user_ids.add(user_id)

    return user_ids


def save_bot_listing_to_disk(user_ids,
                             bot_listing_file_name=None):
    if bot_listing_file_name is None:
        bot_listing_file_name = get_bot_listing_file_name()

    line_separator = '\n'

    lines = line_separator.join(str(user_id) for user_id in user_ids)

    with open(bot_listing_file_name, 'w') as f:
        print(lines, file=f)

    return


def update_and_save_bot_listing_to_disk(user_ids,
                                        bot_listing_file_name=None):
    if bot_listing_file_name is None:
        bot_listing_file_name = get_bot_listing_file_name()

    original_user_ids = load_bot_listing_from_disk(bot_listing_file_name=bot_listing_file_name)

    aggregated_user_ids = set(original_user_ids).union(user_ids)

    save_bot_listing_to_disk(aggregated_user_ids,
                             bot_listing_file_name=bot_listing_file_name)

    return


def main():
    user_ids = download_and_parse_bot_listing()

    return True


if __name__ == '__main__':
    main()
