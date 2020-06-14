def get_my_profile_id():
    my_profile_id = '76561198028705366'

    return my_profile_id


def get_hard_coded_market_dict():
    hard_coded_market_dict = {
        "340390": "Abomination Tower",
        "381640": "Allods Online RU",
        "342250": "Aspectus: Rinascimento Chronicles",
        "636700": "Crappy Day Enhanced Edition",
        "558490": "Crossroad Mysteries: The Broken Deal",
        "318090": "Dicetiny",
        "286240": "Dog Sled Saga",
        "290140": "Echo of Soul",
        "409070": "Fist Slash: Of Ultimate Fury",
        "522340": "Ghostlords",
        "495230": "Hypnorain",
        "398140": "Ino",
        "304170": "Kick-Ass 2",
        "487630": "Lantern",
        "499950": "Metal Assault - Gigaslave - Europe",
        "254880": "MoonBase Commander",
        "383690": "Mu Complex",
        "338340": "Nightbanes",
        "325120": "Notch - The Innocent LunA: Eclipsed SinnerS",
        "298520": "Orbital Gear",
        "514570": "Pinball Parlor",
        "523060": "Planet Smasher",
        "368180": "Polyball",
        "205610": "Port Royale 3",
        "448720": "Puzzle Box",
        "554660": "Puzzle Poker",
        "351090": "Regency Solitaire",
        "272330": "Shadow Blade: Reload",
        "307050": "Shan Gui",
        "324470": "SinaRun",
        "210170": "Spirits",
        "675630": "Super POTUS Trump",
        "276730": "Tango Fiesta",
        "434780": "The Renegades of Orion 2.0",
        "533690": "Think To Die",
        "270010": "Time Rifters",
        "521340": "True or False",
        "486460": "Twilight Town",
        "339000": "Ukrainian Ninja",
        "714050": "Undead",
        "562260": "WAVESHAPER",
        "451230": "Wartune",
        "359400": "Why Am I Dead At Sea",
        "403700": "Zero Punctuation: Hatfall - Hatters Gonna Hat Edition",
        "582350": "Zombie Killin'",
    }

    return hard_coded_market_dict


def sort_dict_by_value(input_dictionary):
    # Reference: https://stackoverflow.com/a/613218

    sorted_dictionary = {
        k: v
        for k, v in sorted(
            input_dictionary.items(),
            key=lambda item: item[1],
        )
    }

    return sorted_dictionary


def main():
    hard_coded_market_dict = get_hard_coded_market_dict()

    sorted_dictionary = sort_dict_by_value(hard_coded_market_dict)

    print(sorted_dictionary)

    return True


if __name__ == '__main__':
    main()
