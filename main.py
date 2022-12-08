from digital_market import DigitalMarket


def helps():
    print(""" 
    digi --like     <product code>
    digi --unlike   <product code>
    digi --add      <product code> <number>     # add to shopping bag
    digi --rm       <product code> <number>     # remove from shopping back
    digi --get-bill
    digi --cancel-process
    digi --back
    """)

def intro():
    while True:
        print("""
        -------------< WELCOME >-------------
        1. Sing-up
        2. Login
        3. Exit
        -------------------------------------
        """)
        
        user_choice = input(">>").strip()

        if user_choice == "1":
            print("-----------------< Sin-up >-----------------")
            full_name = input("Full Name(e.g john-smeeth): ").strip()
            age = input("Age: ").strip()
            user_id = input("ID: ").strip()
            email = input("Email: ").strip()
            phone = input("Phone Number: ").strip()
            password = input("Password(length > 7): ").strip()
            wallet= input("Wallet: ").strip()
            print("--------------------------------------------")
            
            res = DigitalMarket.singup(full_name, user_id, password, age, email, phone, wallet)
            print(res)

        elif user_choice == "2":
            print("-----------------< Sin-up >-----------------")
            user_id = input("ID: ").strip()
            password = input("Password: ").strip()
            print("--------------------------------------------")

            res = DigitalMarket.login(user_id, password)
            if type(res) is str:
                print(res)
            else:
                print("Loggin succussfully.")
                main(res)            
            
        elif user_choice == "3":
            print("Exit...")
            break
        
        else:
            pass

def main(user_object):
    def options():
        print("\n\n")
        print("~~~~~~~~~~~< DIGI MARKET >~~~~~~~~~~~")
        print("1. Profile")
        print("2. My Shopping Bag")
        print("3. My Favorite Products")
        print("4. My Shopping History")
        print("5. Clear History")
        print("6. Categories")
        print("7. Exit")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    
    while True:
        options()
        user_choice = input(">>").strip()

        if user_choice == "1":
            user_object.profile()
            input()
        
        elif user_choice == "2":
            user_object.myShoppingBag()
            input()

        elif user_choice == "3":
            user_object.myFavoriteProducts()
            input()

        elif user_choice == "4":
            user_object.myShoppingHistroy()
            input()

        elif user_choice == "5":
            res = user_object.clearHistory()
            print(res)
            input

        elif user_choice == "6":
            categories = user_object.categories()
            print("~~~~~~~~~~~~< Categories >~~~~~~~~~~~~")
            for Id, name in categories.items():
                print("{}. {}".format(Id, name))
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

            cat_id = input(">>") 

            if cat_id in categories:
                category(user_object, categories[cat_id])
            else:
                print("Input is wrong!")

        elif user_choice == "7":
            print("log out")
            break

def category(user_object, cat):
    pages = user_object.products(cat)
    if type(pages) is str:
        print(pages)
        return None

    while True:    
        print("~~~~~~~~~~~~< Products >~~~~~~~~~~~~")
        for product_code, info in pages.currentPageData().items():
            print("{}. {}".format(product_code, info["Name"]))
            print("Price: {}".format(info["Price"]))
            print("Stock: {}".format(info["Stock"]))
            print()
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("<~~~~~~~~~~~~< {} >~~~~~~~~~~~~>".format(pages.page_number))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Next-Page: --n || Previous-Page: --p")    
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        user_choice = input(">>").strip()

        if user_choice == "--n":
            pages.next_page()

        elif user_choice == "--p":
            pages.previous_page()

        elif user_choice.startswith("digi"):
            user_choice = user_choice.split(" ")
            user_choice = list(filter(lambda a: a != "" ,user_choice))
            user_choice = list(map(lambda a: a.strip(), user_choice))

            if user_choice[0] == "digi":
                user_choice.remove("digi")

                if user_choice == []:
                    print("Error: Command is wrong.")
                
                elif user_choice[0] == "--like":
                    user_choice.remove("--like")
                    
                    if len(user_choice) == 1:
                        res = user_object.addAProductToMyFavorites(cat, user_choice[0])
                        print(res)
                    else:
                        print("Error: try [digi --like <prodict code>]")
                    
                    input()

                elif user_choice[0] == "--unlike":
                    user_choice.remove("--unlike")
                    
                    if len(user_choice) == 1:
                        res = user_object.removeAProductFromMyFavorites(cat, user_choice[0])
                        print(res)
                    else:
                        print("Error: try [digi --unlike <prodict code>]")
                    
                    input()
                        
                elif user_choice[0] == "--add":
                    user_choice.remove("--add")

                    if len(user_choice) == 2:
                        product_code, number = user_choice
                        res = user_object.addAProductToMyShoppingBag(cat, product_code, number)
                        print(res)
                    else:
                        print("Error: try [digi --add <product code> <number>]")
                    
                    input()
                
                elif user_choice[0] == "--rm":
                    user_choice.remove("--rm")

                    if len(user_choice) == 1:
                        res = user_object.removeAProductFromMyShoppingBag(cat, user_choice[0])
                        print(res)
                    else:
                        print("Error: try [digi --rm <product code> <number>]")                   
                    
                    input()
            
                elif user_choice[0] == "--get-bill":
                    user_choice.remove("--get-bill")

                    if len(user_choice) == 0:
                        res = user_object.confirmOrder()
                        print(res)
                    else:
                        print("Error: try [digi --get-bill]")
                
                    input()
                
                elif user_choice[0] == "--cancel-process":
                    user_choice.remove("--cancel-process")

                    if len(user_choice) == 0:
                        res = user_object.cancelOrder()
                        print(res)
                    else:
                        print("Error: try [digi --cancel-process]")

                    input()
                elif user_choice[0] == "--back":
                    return

            else:
               print("Error: Command is wrong.")



if __name__ == "__main__":
    intro()