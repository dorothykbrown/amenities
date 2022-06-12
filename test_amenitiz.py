from amenitiz import Product, Rule, CashRegister
import unittest
import math


class TestCashRegister(unittest.TestCase):

    def test_cash_register_success(self):

        product_gr1 = Product("GR1", "Green Tea", 3.11)
        product_sr1 = Product("SR1", "Strawberries", 5.00)
        product_cf1 = Product("CF1", "Coffee", 11.23)

        product_list = [
            product_gr1,
            product_sr1,
            product_cf1
        ]

        rule_list = [
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
            ),
        ]

        mcb = CashRegister(products=product_list, rules=rule_list)

        baskets = [
            "GR1,GR1",
            "SR1,SR1,GR1,SR1",
            "GR1,CF1,SR1,CF1,CF1",
            "GR1,GR1,GR1,SR1,SR1,CF1,CF1",
            "GR1,GR1,GR1,SR1,SR1,CF1,CF1,CF1",
            ""
        ]

        actual_calculated_total_prices = []
        for basket_str in baskets:
            actual_calculated_total_prices.append(mcb.calculate_total_price(basket_str=basket_str))

        self.assertEqual(
            actual_calculated_total_prices,
            [3.11, 16.61, 30.57, 38.68, 38.68, 0.00],
            "Actual calculated total prices are not as expected"
        )

if __name__ == '__main__':
    unittest.main()