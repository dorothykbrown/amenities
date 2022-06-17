import math
from operator import itemgetter
import unittest

class Product:
    def __init__(self, code, name, price):
        self.code = code
        self.name = name
        self.price = price

    def update(self, name=None, price=None):

        if name is not None:
            self.name = name

        if price is not None:
            self.price = price

    def update_from_code(code=None, name=None, price=None):
        if code is not None:
            product = Product.get(code=code)
            if product is not None:
                self = product
            else:
                raise Exception("Cannot update product with unknown product code")

        if name is not None:
            self.name = name

        if price is not None:
            self.price = price

class Rule:
    def __init__(self, product, func): 
        self.product = product
        self.function = func


class UnknownItemsInBasketError(Exception):
    def __init__(self, unknown_items_list):
        self.unknown_items = unknown_items_list
        super().__init__(f"Unknown items in basket: {self.unknown_items}")


class CashRegister:
    def __init__(self, products, rules=[]):
        self.products = products

        if len(rules) > 0:
            self.rules = rules

        self.product_price_list = {
            product.code: product
            for product in self.products
        }

    def calculate_total_price(self, basket_str):
        total = 0.00
        basket_dict = {}

        if len(basket_str) == 0:
            basket_list = []
        else:
            basket_list = basket_str.split(",")
            self.validate_basket(basket=basket_list)

        for item in basket_list:
            basket_dict.setdefault(item, 0)
            basket_dict[item] += 1
            

        if len(self.rules) > 0:
            for rule in self.rules:
                if rule.product.code in basket_dict:
                    total += rule.function(basket_dict, rule.product)
                    del basket_dict[rule.product.code]

        for item, num_items in basket_dict.items():
            total += self.product_price_list[item].price * num_items

        return round(total, 2)

    def validate_basket(self, basket):
        unknown_items = [
            item
            for item in basket
            if item not in self.product_price_list 
        ]
        if len(unknown_items) > 0:
            raise UnknownItemsInBasketError(unknown_items)

    def get_product(self):
        pass

    def update_product(self):
        pass

    def delete_product(self):
        pass


if __name__ == '__main__':

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

    cr1 = CashRegister(products=product_list, rules=rule_list)
    print(cr1.product_price_list)
    
    basket_list_str = input("Enter a list of products in basket: ")
    
    basket_price = cr1.calculate_total_price(basket=basket_list_str)
    print("Total basket price (in Euros): ", basket_price)


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
        mcb.calculate_total_price(basket=basket_list)

        baskets = [
            "GR1,GR1",
            "SR1,SR1,GR1,SR1",
            "GR1,CF1,SR1,CF1,CF1"
        ]

        actual_calculated_total_prices = []
        for basket in baskets:
            basket_list = basket.split(",")
            actual_calculated_total_prices.append(mcb.calculate_total_price(basket_list))

        self.assertEqual(
            actual_calculated_total_prices,
            [3.11, 16.61, 30.57],
            "Actual calculated total prices are not as expected"
        )

