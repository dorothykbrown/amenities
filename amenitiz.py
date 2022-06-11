

class Product:
    def __init__(self, code, name, price):
        self.code = code
        self.name = name
        self.price = price

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
        for item in basket:
            total += self.product_price_list[item].price

        return total


if __name__ == '__main__':

    product_list = [
        Product("GR1", "Green Tea", 3.11),
        Product("SR1", "Strawberries", 5.00),
        Product("CF1", "Coffee", 11.23)
    ]

    mcb = CashRegister(products=product_list)
    print(mcb.product_price_list)
    
    basket_list_str = input("Enter a list of products in basket: ")
    basket_list = basket_list_str.split(",")
    basket_price = mcb.calculate_total_price(basket=basket_list)
    print("Total basket price: ", basket_price)

    