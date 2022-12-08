import json

class JsServerUser:
    __PATH = "DataServer\\repository\\users.json"

    @classmethod
    def __pull(cls):
        """ 
        thid method return all datas that there are in the __PATH 
        """
        try:
            with open(cls.__PATH, "r") as Js:
                data = json.load(Js)
        except:
            raise Exception("Error [User data service]: Pull data is not possible.")
        else:
            return data
    
    @classmethod # generatore function
    def userIdCollector(cls):
        data = cls.__pull()
        for unique_id, user_info in data.items():
            yield user_info["UserId"]

    @classmethod # generatore function
    def uniqueIdCollector(cls):
        data = cls.__pull()
        for unique_id in data:
            yield unique_id

    @classmethod
    def append(cls, obj):
        data = cls.__pull()
        data.update(obj)
        with open(cls.__PATH, "w") as js:
            json.dump(data, js, indent=4)

    @classmethod    
    def requestForGetUserData(cls, unique_id):
        data = cls.__pull()
        try:
            target = data[unique_id]
        except:
            raise Exception("Error [User data service]: The user don't have any data.")
        else:
            return target

    @classmethod
    def requestForGetTheValueOfAkey(cls, unique_id, key):
        user_data = cls.requestForGetUserData(unique_id)
        try:
            target = user_data[key]
        except:
            raise Exception("Error [User data service]: In the user datas, there is no any {} as key.".format(key))
        else:
            return target

    @classmethod
    def requestForUpdateTheValueOfAkey(cls, unique_id, key, value):
        data = cls.__pull()
        try:
            data[unique_id][key] = value
        except:
            if unique_id not in data:
                raise Exception("Error [User data service]: updating the value of a key is not possible. Unique id not found.")
            else:
                raise Exception("Error [User data service]: updating the value of a key is not possible. key not found.")

        else:
            with open(cls.__PATH, "w") as js:
                json.dump(data, js, indent=4)
    