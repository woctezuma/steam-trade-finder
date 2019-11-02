# The code shown below is an excerpt from:
#   https://github.com/woctezuma/steam-market/blob/master/utils.py


from pathlib import Path


def get_data_folder():
    data_folder = 'data/'
    Path(data_folder).mkdir(exist_ok=True)

    return data_folder


def main():
    return True


if __name__ == '__main__':
    main()
