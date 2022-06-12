from amenitiz import Product, Rule, CashRegister, UnknownItemsInBasketError
import unittest
import math


class TestCashRegister(unittest.TestCase):

    def setUp(self) -> None:
        product_gr1 = Product("GR1", "Green Tea", 3.11)
        product_sr1 = Product("SR1", "Strawberries", 5.00)
        product_cf1 = Product("CF1", "Coffee", 11.23)

        self.product_list = [
            product_gr1,
            product_sr1,
            product_cf1
        ]

        self.rule_list = [
            Rule(
                product=product_gr1, 
                func=lambda basket_dict, product : math.ceil(
                    basket_dict[product.code]/2
                ) * product.price
            ),
            Rule(
                product=product_sr1, 
                func=lambda basket_dict, product : (
                    basket_dict[product.code] * 4.50
                    if basket_dict[product.code] >= 3
                    else basket_dict[product.code] * product.price
                )
            ),
            Rule(
                product=product_cf1, 
                func=lambda basket_dict, product : (
                    basket_dict[product.code] * product.price * 2/3
                    if basket_dict[product.code] >= 3
                    else basket_dict[product.code] * product.price
                )
            )
        ]

        self.cr1 = CashRegister(products=self.product_list, rules=self.rule_list)

    def tearDown(self) -> None:
        self.product_list = []
        self.rule_list = []
        self.cr1 = CashRegister(products=self.product_list, rules=self.rule_list)

    def test_cash_register_success(self):

        baskets = [
            "GR1",
            "GR1,GR1",
            "SR1,SR1,GR1,SR1",
            "GR1,CF1,SR1,CF1,CF1",
            "GR1,GR1,GR1,SR1,SR1,CF1,CF1",
            "GR1,GR1,GR1,SR1,SR1,CF1,CF1,CF1",
            ""
        ]

        actual_calculated_total_prices = []
        for basket_str in baskets:
            actual_calculated_total_prices.append(self.cr1.calculate_total_price(basket_str=basket_str))

        self.assertEqual(
            actual_calculated_total_prices,
            [3.11, 3.11, 16.61, 30.57, 38.68, 38.68, 0.00],
            "Actual calculated total prices are not as expected"
        )

    def test_cash_register_error_unknown_item(self):
        with self.assertRaises(UnknownItemsInBasketError):
            self.cr1.calculate_total_price(basket_str="OR1, PN1")
        

if __name__ == '__main__':
    unittest.main()