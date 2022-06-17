# Amenitiz

For this simple application I created separate classes for the CashRegister, Product and Rules. 

The Product and Rule classes would allow new products and rules instances to be easily created. With a database, these classes would be models.

The CashRegister class contains a dictonary of active products and rules, so that product and rule instances can be quickly retrieved by the their code. This class also contains the method to calculate the total price of the items in a given basket, applying the rules belonging to a cash register instance.  Additionally this class has methods to validate that items in a basket are valid products that belong to the CashRegister instance, and methods for updating the products and rules associated with the CashRegister instance.

There is as test file that tests the functionality of the function to calculate the total price of the items in a basket for the product and rules given in the problem statement as well as tests to check the functionality of the helper methods for getting, updating, adding and deleting produts and rules from a cash register instance for both success and error cases. 
