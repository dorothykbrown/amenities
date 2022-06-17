from amenitiz import CannotAddModelInstanceWithExistingCodesError, Product, Rule, CashRegister, UnknownItemsInBasketError, UnknownModelInstanceError
import unittest
import math


class TestCashRegister(unittest.TestCase):

    def setUp(self) -> None:
        self.product_gr1 = Product("GR1", "Green Tea", 3.11)
        self.product_sr1 = Product("SR1", "Strawberries", 5.00)
        product_cf1 = Product("CF1", "Coffee", 11.23)

        self.product_list = [
            self.product_gr1,
            self.product_sr1,
            product_cf1
        ]

        self.gr1_rule_function = lambda basket_dict, product : math.ceil(
            basket_dict[product.code]/2
        ) * product.price

        self.gr1_rule = Rule(
            code="GR1:Buy1Get1",
            product=self.product_gr1,
            func=self.gr1_rule_function
        )
        self.sr1_rule = Rule(
            code="SR1:3+RedPrice",
            product=self.product_sr1, 
            func=lambda basket_dict, product : (
                basket_dict[product.code] * 4.50
                if basket_dict[product.code] >= 3
                else basket_dict[product.code] * product.price
            )
        )

        self.rule_list = [
            self.gr1_rule,
            self.sr1_rule,
            Rule(
                code="CF1:3+RedPrice",
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

    def test_get_product_from_cash_register_success(self):

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

    def test_get_product_from_cash_register_error(self):
        
        product = self.cr1.get_product("BL1")
        self.assertEqual(product, None, "Product retrieved is not as expected")
       

    def test_add_product_to_cash_register(self):
        mango_product = Product("MG1", "Mango", 1.50)

        green_tea_product = self.cr1.get_product("GR1")
        strawberry_product = self.cr1.get_product("SR1")
        existing_products = [green_tea_product, strawberry_product]

        existing_product_codes = [green_tea_product.code, strawberry_product.code]

        products_to_add = existing_products + [mango_product]

        with self.assertRaises(
            CannotAddModelInstanceWithExistingCodesError,
            msg=str(
                CannotAddModelInstanceWithExistingCodesError(model=Product, codes=existing_product_codes)
            )
        ):
            self.cr1.add_products(products_to_add)
        
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

    def test_update_product_in_cash_register_success(self):

        self.cr1.update_product(code="GR1", price=4.22)

        product3 = self.cr1.get_product(code="GR1")
    
        self.assertEqual(
            product3.price,
            4.22,
            "Actual product3 price is not as expected"
        )

    def test_update_product_in_cash_register_error(self):

        with self.assertRaises(
            UnknownModelInstanceError,
            msg=str(
                UnknownModelInstanceError(model=Product, code="BL1")
            )
        ):
            self.cr1.update_product(code="BL1", name="Blueberry")
        

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

    def test_update_rule(self):
        product_gp1 = Product("GP1", "Grape", 0.80)

        rule1 = Rule("GP1:HalfOff", self.product_gr1, lambda basket_dict, product: (
            basket_dict[product.code] * product.price * 0.5
        ))

        rule1.update(product=product_gp1)

        self.assertEqual(
            {
                "code": rule1.code,
                "product": rule1.product,
            },
            {
                "code": "GP1:HalfOff",
                "product": product_gp1,
            },
            "rule1 retrieved is not as expected"
        )

    def test_get_rule_from_cash_register_success(self):

        green_tea_rule = self.cr1.get_rule("GR1:Buy1Get1")
        
        self.assertEqual(
            {
                "code": green_tea_rule.code,
                "product": green_tea_rule.product,
                "function": green_tea_rule.function
            },
            {
                "code": "GR1:Buy1Get1",
                "product": self.product_gr1,
                "function": self.gr1_rule_function
            },
            "rule1 retrieved is not as expected"
        )

    def test_get_rule_from_cash_register_error(self):
        
        rule = self.cr1.get_rule("MG1:HalfOff")
        self.assertEqual(rule, None, "Rule retrieved is not as expected")
       

    def test_add_rule_to_cash_register(self):
        mango_product = Product("MG1", "Mango", 1.50)

        mango_rule_function = lambda basket_dict, product: (
            basket_dict[product.code] * product.price * 0.5
        )
        mango_rule = Rule("MG1:HalfOff", mango_product, mango_rule_function)

        existing_rules = [self.gr1_rule, self.sr1_rule]

        existing_rules_codes = [self.gr1_rule.code, self.sr1_rule.code]

        rules_to_add = existing_rules + [mango_rule]

        with self.assertRaises(
            CannotAddModelInstanceWithExistingCodesError,
            msg=str(
                CannotAddModelInstanceWithExistingCodesError(model=Product, codes=existing_rules_codes)
            )
        ):
            self.cr1.add_rules(rules_to_add)
        
        rule_from_cr = self.cr1.get_rule(code=mango_rule.code)

        self.assertEqual(
            {
                "code": rule_from_cr.code,
                "product": rule_from_cr.product,
                "function": rule_from_cr.function
            },
            {
                "code": "MG1:HalfOff",
                "product": mango_product,
                "function": mango_rule_function
            },
            "mango_rule retrieved is not as expected"
        )

    def test_update_rule_in_cash_register_success(self):

        mango_product = Product("MG1", "Mango", 1.50)

        self.cr1.update_rule(code="GR1:Buy1Get1", product=mango_product)

        updated_rule = self.cr1.get_rule(code="GR1:Buy1Get1")
    
        self.assertEqual(
            {
                "code": updated_rule.code,
                "product": updated_rule.product,
            },
            {
                "code": "GR1:Buy1Get1",
                "product": mango_product,
            },
            "updated_rule retrieved is not as expected"
        )

    def test_update_rule_in_cash_register_error(self):

        updated_mango_rule_function = lambda basket_dict, product: (
            basket_dict[product.code] * product.price * 0.5
        )

        with self.assertRaises(
            UnknownModelInstanceError,
            msg=str(
                UnknownModelInstanceError(model=Rule, code="MG1:HalfOff")
            )
        ):
            self.cr1.update_rule(code="MG1:HalfOff", func=updated_mango_rule_function)
        

    def test_delete_rule_from_cash_register(self):
        self.assertEqual(
            set(self.cr1.rules_dict.keys()),
            set(
                ["GR1:Buy1Get1","SR1:3+RedPrice","CF1:3+RedPrice"]
            ),
            "Set of rule codes before delete is not as expected"
        )

        self.cr1.delete_rule("GR1:Buy1Get1")

        self.assertEqual(
            set(self.cr1.rules_dict.keys()),
            set(["SR1:3+RedPrice","CF1:3+RedPrice"]),
            "Set of actual rule codes after delete is not as expected"
        )
        

if __name__ == '__main__':
    unittest.main()