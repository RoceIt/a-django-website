import unittest

from .cart import Cart, ALL

ITEM_A = 'A'
ITEM_B = 'B'
INFO_1 = 1
INFO_2 = 2


class TestCartMethods(unittest.TestCase):

    def setUp(self):
        self.cart = Cart()
        self.filled_cart = Cart()
        self.filled_cart.add_items(ITEM_A, 1, INFO_1)
        self.filled_cart.add_items(ITEM_A, 2, INFO_2)
        self.filled_cart.add_items(ITEM_B, 3, INFO_1)
        self.filled_cart.add_items(ITEM_B, 4, INFO_2)
        self.filled_cart.add_items(ITEM_A, 1)

    def test_assert_new_cart_is_empty(self):
        self.assertEqual(self.cart.count(ALL), 0)

    def test_add_object_without_info(self):
        self.cart.add_items(ITEM_A, 1)
        self.assertEqual(self.cart.count(ALL), 1)
        self.assertEqual(self.cart.count(ITEM_A), 1)

    def test_add_2_equal_objects_without_info(self):
        self.cart.add_items(ITEM_A, 1)
        self.cart.add_items(ITEM_A, 2)
        self.assertEqual(self.cart.count(ALL), 3)
        self.assertEqual(self.cart.count(ITEM_A), 3)

    def test_add_2_different_objects_without_info(self):
        self.cart.add_items(ITEM_A, 1)
        self.cart.add_items(ITEM_B, 2)
        self.assertEqual(self.cart.count(ALL), 3)
        self.assertEqual(self.cart.count(ITEM_A), 1)
        self.assertEqual(self.cart.count(ITEM_B), 2)

    def test_add_object_with_info(self):
        self.cart.add_items(ITEM_A, 1, INFO_1)
        self.assertEqual(self.cart.count(ALL), 1)
        self.assertEqual(self.cart.count(ITEM_A, ALL), 1)
        self.assertEqual(self.cart.count(ITEM_A, INFO_1), 1)

    def test_add_2_equal_objects_with_equal_info(self):
        self.cart.add_items(ITEM_A, 1, INFO_1)
        self.cart.add_items(ITEM_A, 2, INFO_1)
        self.assertEqual(self.cart.count(ALL), 3)
        self.assertEqual(self.cart.count(ITEM_A, ALL), 3)
        self.assertEqual(self.cart.count(ITEM_A, INFO_1), 3)

    def test_add_2_equal_objects_with_different_info(self):
        self.cart.add_items(ITEM_A, 1, INFO_1)
        self.cart.add_items(ITEM_A, 2, INFO_2)
        self.assertEqual(self.cart.count(ALL), 3)
        self.assertEqual(self.cart.count(ITEM_A, ALL), 3)
        self.assertEqual(self.cart.count(ITEM_A, INFO_1), 1)
        self.assertEqual(self.cart.count(ITEM_A, INFO_2), 2)

    def test_add_2_different_objects_with_equal_info(self):
        self.cart.add_items(ITEM_A, 1, INFO_1)
        self.cart.add_items(ITEM_B, 2, INFO_1)
        self.assertEqual(self.cart.count(ALL), 3)
        self.assertEqual(self.cart.count(ITEM_A, ALL), 1)
        self.assertEqual(self.cart.count(ITEM_B, ALL), 2)
        self.assertEqual(self.cart.count(ITEM_A, INFO_1), 1)
        self.assertEqual(self.cart.count(ITEM_B, INFO_1), 2)

    def test_add_2_different_objects_with_different_info(self):
        self.cart.add_items(ITEM_A, 1, INFO_1)
        self.cart.add_items(ITEM_B, 2, INFO_2)
        self.assertEqual(self.cart.count(ALL), 3)
        self.assertEqual(self.cart.count(ITEM_A, ALL), 1)
        self.assertEqual(self.cart.count(ITEM_B, ALL), 2)
        self.assertEqual(self.cart.count(ITEM_A, INFO_1), 1)
        self.assertEqual(self.cart.count(ITEM_B, INFO_2), 2)

    def test_add_2_different_objects_with_different_info_each(self):
        self.cart.add_items(ITEM_A, 1, INFO_1)
        self.cart.add_items(ITEM_A, 2, INFO_2)
        self.cart.add_items(ITEM_B, 3, INFO_1)
        self.cart.add_items(ITEM_B, 4, INFO_2)
        self.assertEqual(self.cart.count(ALL), 10)
        self.assertEqual(self.cart.count(ITEM_A, ALL), 3)
        self.assertEqual(self.cart.count(ITEM_B, ALL), 7)
        self.assertEqual(self.cart.count(ITEM_A, INFO_1), 1)
        self.assertEqual(self.cart.count(ITEM_A, INFO_2), 2)
        self.assertEqual(self.cart.count(ITEM_B, INFO_1), 3)
        self.assertEqual(self.cart.count(ITEM_B, INFO_2), 4)

    def test_clear_cart(self):
        self.filled_cart.clear()
        self.assertEqual(self.cart.count(ALL), 0)

    def test_remove_all_objects_of_one_kind(self):
        self.filled_cart.remove_items(ITEM_A, ALL, ALL)
        self.assertEqual(self.filled_cart.count(ALL), 7)
        self.assertEqual(self.filled_cart.count(ITEM_B, ALL), 7)
        self.assertEqual(self.filled_cart.count(ITEM_A, ALL), 0)

    def test_remove_one_objects_of_one_kind(self):
        self.filled_cart.remove_items(ITEM_A, 1)
        self.assertEqual(self.filled_cart.count(ALL), 10)
        self.assertEqual(self.filled_cart.count(ITEM_B, ALL), 7)
        self.assertEqual(self.filled_cart.count(ITEM_A, ALL), 3)
        self.assertEqual(self.filled_cart.count(ITEM_A, INFO_1), 1)
        self.assertEqual(self.filled_cart.count(ITEM_A, INFO_2), 2)
        self.assertEqual(self.filled_cart.count(ITEM_A, None), 0)
        print(type(self.filled_cart))

    # def test_remove_one_object_of_one_kind(self):
    #     self.filled_cart.remove_items(ITEM_B1, )
