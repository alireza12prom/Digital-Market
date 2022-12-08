from DataServer.UserDataManagement import JsServerUser
from user import User
import random

class DigitalMarket:
    
    @classmethod
    def singup(cls, full_name, user_id, password, age, email, phone, wallet):
        """ full_name: name-family """
        try:
            full_name = cls.__singup_full_name_validation(full_name)
            user_id = cls.__singup_user_id_validation(user_id)
            password = cls.__singup_password_validation(password)
            age = cls.__singup_age_validation(age)
            email = cls.__singup_email_validation(email)
            phone = cls.__singup_phone_validation(phone)
            wallet = cls.__singup_wallet_validation(wallet)
        except Exception as err:
            return err
        else:
            json_form ={
                cls.__unique_id():{
                    "FullName": full_name,
                    "UserId": user_id,
                    "Password":password,
                    "Age": age,
                    "Email": email,
                    "Phone": phone,
                    "Wallet": wallet,
                    "ShoppingBag": {},
                    "Favorites": {},
                    "ShoppingHistory": {}
                }
            }
            JsServerUser.append(json_form)
            return "Create you new account successfully. now, login to your account."

    @classmethod
    def login(cls, user_id, password):
        unique_ids = JsServerUser.uniqueIdCollector()
        for unique_id in unique_ids:
            user = JsServerUser.requestForGetUserData(unique_id)
            if (user["UserId"] == user_id):
                if (user["Password"] == password):
                    return User(unique_id)
                else:
                    return "Password is wrong."
        return "You don't have any account with this ID."
    

    @staticmethod
    def __unique_id():
        while True:
            target = random.randint(1000, 9999)
            for unique_id in JsServerUser.uniqueIdCollector():
                if str(target) == unique_id:
                    break
            else: # if str(target) != unique_id
                return str(target)

    # Sing-up validation
    @staticmethod
    def __singup_full_name_validation(target):
        try:
            name, family = target.split("-")
            if (len(name) == 0) or (len(family) == 0):
                raise Exception
        
        except ValueError:
            raise Exception("Name and family must be detach with a '-'.")
        
        except Exception:
            raise Exception("Name or Family is an empty string.")
        
        else:
            return target
    
    @staticmethod
    def __singup_user_id_validation(target):
        for user_id in JsServerUser.userIdCollector():
            if user_id == target:
                raise Exception("The ID has already been used.")
        
        return target

    @staticmethod
    def __singup_password_validation(target):
        if len(target) >= 8:
            return target
        else:
            raise Exception("The password length must be greater than 7 characters.")
    
    @staticmethod
    def __singup_age_validation(target) ->int:
        try:
            target = int(target)
        except:
            raise Exception("Your age must be an integer.")
        else:
            return target

    @staticmethod
    def __singup_email_validation(target):
        email_prefixes = ["gmail.com", "yahoo.com", "email.com"]
        try:
            email, prefix = target.split("@")
            if (len(email) == 0) or (len(prefix) == 0):
                raise ValueError
            elif prefix not in email_prefixes:
                raise Exception
        
        except ValueError:
            raise Exception("Email is wrong")
        
        except Exception:
            raise Exception("The prefix must be: {}".format(", ".join(email_prefixes)))
        
        else:
            return target

    @staticmethod
    def __singup_phone_validation(target) ->int:
        try:
            target = int(target)
        except:
            raise Exception("The number must be a sequence of numbers.")
        else:
            return target
    
    @staticmethod
    def __singup_wallet_validation(target) ->int:
        try:
            target = int(target)
        except:
            raise Exception("something went wrong.")
        else:
            return target

