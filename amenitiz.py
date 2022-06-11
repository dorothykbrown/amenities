import math

class Product:
    def __init__(self, code, name, price):
        self.code = code
        self.name = name
        self.price = price

class Rule:
    def __init__(self, product, func): 
        self.product = product
        self.function = func

class CashRegister:
    def __init__(self, products, rules=[]):
        self.products = products

        if len(rules) > 0:
            self.rules = rules

        self.product_price_list = {
            product.code: product
            for product in self.products
        }



    def calculate_total_price(self, basket):
        total = 0.00
        basket_dict = {}

        for item in basket:
            basket_dict.setdefault(item, 0)
            basket_dict[item] += 1
            

        if len(self.rules) > 0:
            for rule in self.rules:
                total += rule.function(basket_dict, rule.product)
                del basket_dict[rule.product.code]

        for item, num_items in basket_dict.items():
            total += self.product_price_list[item].price * num_items

        return total


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
    ]

    mcb = CashRegister(products=product_list, rules=rule_list)
    print(mcb.product_price_list)
    
    basket_list_str = input("Enter a list of products in basket: ")
    basket_list = basket_list_str.split(",")
    basket_price = mcb.calculate_total_price(basket=basket_list)
    print("Total basket price: ", basket_price)

    