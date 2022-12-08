from Interface.User import UserInterface
from DataServer.UserDataManagement import JsServerUser
from DataServer.ProductDataManagement import JsServerProduct
from category import Category
from datetime import datetime

# Rule:
#   Each order reaches the customer after 3 days
#   lowered 10% of the amount of payment from the total amount paid

class User():
    # when an order is canceled, we will lower 10%
    # of the amount of payment from the total amount paid.    
    __returnedTheAmountPaid = 10 

    def __init__(self, Id):
        # this is a unique id
        self.__id = Id

    def profile(self):
        data = JsServerUser.requestForGetUserData(self.__id)
        print("User-Id: {} \nFull-Name: {} \nAge: {} \nEmail: {} \nPhone: {} \nWallet: {}$".format(
            data["UserId"], data["FullName"], data["Age"], data["Email"], data["Phone"], data["Wallet"] 
        ))
    
    def myShoppingBag(self):
        shoppint_bag_data = JsServerUser.requestForGetTheValueOfAkey(self.__id, "ShoppingBag")
        
        if shoppint_bag_data == {}:
            print("Your shopping bag is empty yet.")
        else:
        
            # in shoppin bag every item is a structure something like:
            #    productCode: {Category: value, number: value}, ...
            total = 0
            for product_code in shoppint_bag_data:

                category, number = shoppint_bag_data[product_code]["Category"], shoppint_bag_data[product_code]["Number"]
                product_data = JsServerProduct.requestForGetAProduct(category, product_code)
                print(">>>>> {}\{};".format(category, product_data["Name"]))
                print("Product Id: {}".format(product_code))
                print("Price: {}$".format(product_data["Price"]))
                print("Number: {}".format(number))
                if product_data["Stock"] == 0:
                    print("\\ Is not available!")
                elif product_data["Stock"] < number:
                    print("\\ The number of available is {}!".format(product_data["Stock"]))
                total += (product_data["Price"] * number)
                print()
            print("="*20)
            print("Total: {}$".format(total))
            
    def myFavoriteProducts(self):
        favorites_list = JsServerUser.requestForGetTheValueOfAkey(self.__id, "Favorites")

        if len(favorites_list) == 0:
            print("You don't have favorites product.")
        else:
            # in favorites list every item has an structure something like:
            #       {"ProductCode":"Category", ..}
            for product_code, category in favorites_list.items():
                product_data = JsServerProduct.requestForGetAProduct(category, product_code)
                print(">>>>> {}\{};".format(category, product_data["Name"]))
                print("Product Id: {}".format(product_code))
                print("Price: {}$".format(product_data["Price"]))
                print("stock: {}".format(product_data["Stock"]))
                print()

    def myShoppingHistroy(self):
        shopping_history = JsServerUser.requestForGetTheValueOfAkey(self.__id, "ShoppingHistory")
        if len(shopping_history) != 0:
            for key, orders in shopping_history.items():
                
                order_id, order_date, order_state = key.split("-")
                print(">>> {} - {} at {};".format(order_id, order_state, order_date))
                
                bill = sum([item["Bill"] for item in orders])
                for item in orders:
                    product = JsServerProduct.requestForGetAProduct(item["Category"], item["ProductCode"])
                    print("    ", "Name: {} - Number: {} - The price of each one: {}".format(product["Name"], item["Number"], product["Price"]))
                
                print("")
                if order_state == "Posted":
                    print("    ", "Bill: {}".format(bill))
                else:
                    bill -= (self.__returnedTheAmountPaid / 100) * bill
                    print("    ", "Returned amount(Taking {}% tax): {}".format(self.__returnedTheAmountPaid, bill))
                print("")

        else:
            print("Your history is empty yet!")
    
    @staticmethod
    def categories():
        categories = JsServerProduct.requestForGetAListOfCategories()
        return {str(i+1):categories[i] for i in range(len(categories))}

    @classmethod
    def products(cls, category):
        try:
            category = cls.__category_validation(category) 
        except Exception as err:
            return err
        else:
            products = JsServerProduct.requestForGetAListOfProducs(category)
            if products == {}:
                return "ApplicationError: There is no any product for this category."
            else:         
                return Category().fromItems(products)

    def addAProductToMyFavorites(self, category, product_code):
        try:
            category = self.__category_validation(category)
            product_code = self.__product_validation(category, product_code)
        except Exception as err:
            return err
        else:
            favorites_list = JsServerUser.requestForGetTheValueOfAkey(self.__id, "Favorites")
            if product_code not in favorites_list:
                favorites_list.update({product_code:category})
                JsServerUser.requestForUpdateTheValueOfAkey(self.__id, "Favorites", favorites_list)
                
                product = JsServerProduct.requestForGetAProduct(category, product_code)
                return "The product '{}' added to your favorites list.".format(product["Name"])
            else:
                return "The product '{}' already added to your favorites list.".format(product_code)
    
    def removeAProductFromMyFavorites(self, category, product_code):
        try:
            category = self.__category_validation(category)
            product_code = self.__product_validation(category, product_code)
        except Exception as err:
            return err
        else:
            favorites_list = JsServerUser.requestForGetTheValueOfAkey(self.__id, "Favorites")
            if product_code in favorites_list:
                favorites_list.pop(product_code)
                JsServerUser.requestForUpdateTheValueOfAkey(self.__id, "Favorites", favorites_list)
                
                product = JsServerProduct.requestForGetAProduct(category, product_code)
                return "The product '{}' deleted from your favorites list.".format(product["Name"])
            else:
                return "The product '{}' is not in your favorites list.".format(product_code)

    def addAProductToMyShoppingBag(self, category, product_code, number):
        try:
            category = self.__category_validation(category)
            product_code = self.__product_validation(category, product_code)
            number = int(number)
            if number <= 0:
                raise ValueError()
        except ValueError:
            return "InputError: The number of products, must be an integer greater than 0."
        except Exception as err:
            return err
        else:
            shopping_bag = JsServerUser.requestForGetTheValueOfAkey(self.__id, "ShoppingBag")
            if product_code not in shopping_bag:
                shopping_bag.update({product_code:{"Category":category, "Number":number}})
                JsServerUser.requestForUpdateTheValueOfAkey(self.__id, "ShoppingBag", shopping_bag)
                return "The product added successfully"
            else:
                return "You have already added this product to your shoppint bag."
    
    def removeAProductFromMyShoppingBag(self, category, product_code):
        try:
            category = self.__category_validation(category)
            product_code = self.__product_validation(category, product_code)
        except Exception as err:
            return err
        else:
            shopping_bag = JsServerUser.requestForGetTheValueOfAkey(self.__id, "ShoppingBag")
            if product_code in shopping_bag:
                shopping_bag.pop(product_code)
                JsServerUser.requestForUpdateTheValueOfAkey(self.__id, "ShoppingBag", shopping_bag)
                return "The product deleted successfully"
            else:
                return "You don't have this product to your shoppint bag."

    def confirmOrder(self):
        shopping_bag = JsServerUser.requestForGetTheValueOfAkey(self.__id, "ShoppingBag")
        if len(shopping_bag) != 0:
            
            total = 0
            # check the user request 
            for product_code, data in shopping_bag.items():
                product = JsServerProduct.requestForGetAProduct(data["Category"], product_code)
                if data["Number"] > product["Stock"]:
                    return "Error: Of the product '{}' remains only '{}', but your request is '{}'!".format(product["Name"], product["Stock"], data["Number"])
                
                total += (data["Number"] * product["Price"])
            
            # check user inventory
            wallet = JsServerUser.requestForGetTheValueOfAkey(self.__id, "Wallet")
            if total <= wallet:

                # change the stocks
                for product_code, data in shopping_bag.items():
                    product = JsServerProduct.requestForGetAProduct(data["Category"], product_code)
                    product["Stock"] -= data["Number"]
                    JsServerProduct.requestForUpdateTheValueOfAkey(data["Category"], product_code, "Stock", product["Stock"])
                
                # calculate bill
                wallet -= total
                JsServerUser.requestForUpdateTheValueOfAkey(self.__id, "Wallet", wallet)

                # store in history
                # The structure for store:
                # "Id-Date":[
                #       {"ProductCode":"", "Category":"", "Number":0, "Bill":0},
                #       ...
                # ]
                now = datetime.now()
                date = "{}.{}.{}".format(now.day, now.month, now.year)
                history = []
                for product_code, data in shopping_bag.items():
                    product = JsServerProduct.requestForGetAProduct(data["Category"], product_code)
                    json_form = {"ProductCode":product_code, "Category":data["Category"], "Number":data["Number"], "Bill":(data["Number"] * product["Price"])}
                    history.append(json_form)
                
                shopping_history = JsServerUser.requestForGetTheValueOfAkey(self.__id, "ShoppingHistory")

                last_id = len(shopping_history)
                shopping_history.update({
                    "{}-{}-Posted".format(last_id+1, date):history})
                
                JsServerUser.requestForUpdateTheValueOfAkey(self.__id, "ShoppingHistory", shopping_history)

                # clear shopping bag
                JsServerUser.requestForUpdateTheValueOfAkey(self.__id, "ShoppingBag", {})
                
                return "Your order has been successfully recorded. Your bill: {}".format(total)
            else:
                return "Your inventory is not enough (Your enventory: {}, your bill: {}).".format(wallet, total)
        else:
            return "You don't choose any item for buy yet."

    def cancelOrder(self):
        shopping_history = JsServerUser.requestForGetTheValueOfAkey(self.__id, "ShoppingHistory")
        if len(shopping_history) != 0:
            
            shopping_bag = JsServerUser.requestForGetTheValueOfAkey(self.__id, "ShoppingBag")
            if len(shopping_bag) == 0:
                
                # get the last order that stored in the shopping history
                # items in shopping history:
                #   key: "Id-date-state"
                #   value: a list of all orders
                key, last_order = shopping_history.popitem()
                try:
                    key = self.__cancelOrder_validation(key)
                
                except Exception as err:
                    return err
                
                else:

                    # set the last order as 'Returned'
                    order_Id, order_date, order_state = key.split("-")
                    
                    now = datetime.now()
                    returned_date = "{}.{}.{}".format(now.day, now.month, now.year)
        
                    shopping_history.update({
                        "{}-{}-{}".format(order_Id, returned_date, "Returned"):last_order}) 
                    JsServerUser.requestForUpdateTheValueOfAkey(self.__id, "ShoppingHistory", shopping_history)

                    # return the orders to shopping bag
                    bill = 0
                    for order in last_order:
                        shopping_bag.update({order["ProductCode"]:{"Category":order["Category"], "Number":order["Number"]}})
                        bill += order["Bill"]
                    JsServerUser.requestForUpdateTheValueOfAkey(self.__id, "ShoppingBag", shopping_bag)

                    # return the amount paid
                    bill -= (self.__returnedTheAmountPaid / 100) * bill
                    wallet = JsServerUser.requestForGetTheValueOfAkey(self.__id, "Wallet")
                    wallet += bill
                    JsServerUser.requestForUpdateTheValueOfAkey(self.__id, "Wallet", wallet)

                    # return the product stocks
                    for order in last_order:
                        product_stock = JsServerProduct.requestForGetAProduct(order["Category"], order["ProductCode"])["Stock"]
                        product_stock += order["Number"]
                        JsServerProduct.requestForUpdateTheValueOfAkey(order["Category"], order["ProductCode"], "Stock", product_stock)
                    
                    return "Your last order recorded in {} and canceled successfully. \nThe amount returned(Taking {}% tax): {}".format(
                        order_date, self.__returnedTheAmountPaid, bill 
                        )
            else:
                return "Your shopping bag is not empty!"
        else:
            return "You have not any order yet!"

    def clearHistory(self):
        shopping_history = JsServerUser.requestForGetTheValueOfAkey(self.__id, "ShoppingHistory")
        if len(shopping_history) != 0:
            JsServerUser.requestForUpdateTheValueOfAkey(self.__id, "ShoppingHistory", dict())
            return "Your history has been deleted."
        else:
            return "Your history is empty yet!"

    @staticmethod
    def __category_validation(category):
        if category in JsServerProduct.requestForGetAListOfCategories():
            return category
        else:
            raise Exception("InputError: Category '{}' not found.".format(category))
    
    @classmethod
    def __product_validation(cls, category, product_code):
        try:
            category = cls.__category_validation(category)
        except Exception as err:
            raise err
        else:
            if product_code in JsServerProduct.requestForGetAListOfProducs(category):
                return product_code
            else:
                raise Exception("InputError: The product '{}' is not in the category '{}'.".format(product_code, category))

    @staticmethod
    def __cancelOrder_validation(value):
        order_id, order_date, order_state = value.split("-")
        if order_state == "Posted":
            
            day, month, year = order_date.split(".")
            day, month, year = int(day), int(month), int(year)
            now = datetime.now()
            
            if month == now.month and year == now.year:
                if now.day - day > 3:
                    raise Exception(
                        "Your order delivery has been completed (your last order {} days ago). \nYou shoud apply before 3 days.".format(
                            now.day - day))
            
            return value
        else:
            raise Exception("Your last order returned in {}.".format(order_date))

