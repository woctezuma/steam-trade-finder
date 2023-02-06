import unittest

import data_utils
import display_results
import download_bot_listing
import inventory_utils
import personal_info
import trade_finder
import utils


class TestPersonalInfoMethods(unittest.TestCase):
    def test_main(self):
        assert personal_info.main()


class TestUtilsMethods(unittest.TestCase):
    def test_main(self):
        assert utils.main()


class TestInventoryUtilsMethods(unittest.TestCase):
    def test_main(self):
        assert inventory_utils.main()


class TestDownloadBotListingMethods(unittest.TestCase):
    def test_main(self):
        assert download_bot_listing.main()


class TestTradeFinderMethods(unittest.TestCase):
    def test_main(self):
        assert trade_finder.main(self_test=True)


class TestDataUtilsMethods(unittest.TestCase):
    def test_main(self):
        assert data_utils.main()


class TestDisplayResultsMethods(unittest.TestCase):
    def test_main(self):
        assert display_results.main()


if __name__ == '__main__':
    unittest.main()
