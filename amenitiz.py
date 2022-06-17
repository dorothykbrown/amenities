import math

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

    def product_price_dict(self):
        return {
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
            total += self.product_price_dict()[item].price * num_items

        return round(total, 2)

    def validate_basket(self, basket):
        unknown_items = [
            item
            for item in basket
            if item not in self.product_price_dict()
        ]
        if len(unknown_items) > 0:
            raise UnknownItemsInBasketError(unknown_items)

    def get_product(self, code):
        for product in self.products:
            if product.code == code:
                return product

        return None

    
    def add_products(self, products):

        product_codes_to_update = []

        for product in products:
            if product.code not in self.product_price_dict():
                self.products.append(product)
            else:
                product_codes_to_update.append(product.code)

        if len(product_codes_to_update) > 0:
            raise Exception("The products with the following codes already exist: %s", str(product_codes_to_update))


    def update_product(self, code, name=None, price=None):
        product = self.get_product(code)

        if product is not None:
            product.update(name=name, price=price)
            print(f"Product {product.name} ({code}) was updated.")

    def delete_product(self, code):
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
    print(cr1.product_price_dict())
    
    basket_list_str = input("Enter a list of products in basket: ")
    
    basket_price = cr1.calculate_total_price(basket=basket_list_str)
    print("Total basket price (in Euros): ", basket_price)
