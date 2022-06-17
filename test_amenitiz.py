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
        with self.assertRaises(
            UnknownItemsInBasketError,
            msg=str(
                UnknownItemsInBasketError(['OR1', 'PN1'])
            )
        ):
            self.cr1.calculate_total_price(basket_str="OR1,PN1")

    
    def test_update_product(self):
        product1 = Product("OR1", "Orange", 2.50)

        product1.update(name="Valencia Orange")

        self.assertEqual(
            product1.name,
            "Valencia Orange",
            "Actual product1 name is not as expected"
        )

        self.assertEqual(
            product1.price,
            2.50,
            "Actual product1 price is not as expected"
        )

        product2 = Product("PN1", "Pineapple", 4.25)

        product2.update(price=3.75)

        self.assertEqual(
            product2.name,
            "Pineapple",
            "Actual product2 name is not as expected"
        )

        self.assertEqual(
            product2.price,
            3.75,
            "Actual product2 price is not as expected"
        )

    def test_get_product_from_cash_register(self):

        green_tea_product = self.cr1.get_product("GR1")
        
        self.assertEqual(
            {
                "code": green_tea_product.code,
                "name": green_tea_product.name,
                "price": green_tea_product.price
            },
            {
                "code": "GR1",
                "name": "Green Tea",
                "price": 3.11
            },
            "green_tea_product retrieved is not as expected"
        )

    def test_add_product_to_cash_register(self):

        mango_product = Product("MG1", "Mango", 1.50)
        
        self.cr1.add_products([mango_product])

        product_from_cr = self.cr1.get_product(code=mango_product.code)

        self.assertEqual(
            {
                "code": product_from_cr.code,
                "name": product_from_cr.name,
                "price": product_from_cr.price
            },
            {
                "code": "MG1",
                "name": "Mango",
                "price": 1.50
            },
            "mango_product retrieved is not as expected"
        )

    def test_update_product_in_cash_register(self):

        self.cr1.update_product(code="GR1", price=4.22)

        product3 = self.cr1.get_product(code="GR1")
    
        self.assertEqual(
            product3.price,
            4.22,
            "Actual product3 price is not as expected"
        )

    def test_delete_product_from_cash_register(self):
        self.assertEqual(
            set(self.cr1.products_dict.keys()),
            set(
                ["GR1","SR1","CF1"]
            ),
            "Set of product codes before delete is not as expected"
        )

        self.cr1.delete_product("GR1")

        self.assertEqual(
            set(self.cr1.products_dict.keys()),
            set(["SR1","CF1"]),
            "Set of actual product codes after delete is not as expected"
        )
        

if __name__ == '__main__':
    unittest.main()