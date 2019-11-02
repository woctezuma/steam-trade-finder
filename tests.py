import unittest

import inventory_utils
import personal_info
import trade_finder
import utils


class TestPersonalInfoMethods(unittest.TestCase):

    def test_main(self):
        self.assertTrue(personal_info.main())


class TestUtilsMethods(unittest.TestCase):

    def test_main(self):
        self.assertTrue(utils.main())


class TestInventoryUtilsMethods(unittest.TestCase):

    def test_main(self):
        self.assertTrue(inventory_utils.main())


class TestTradeFinderMethods(unittest.TestCase):

    def test_main(self):
        self.assertTrue(trade_finder.main(self_test=True))


if __name__ == '__main__':
    unittest.main()
