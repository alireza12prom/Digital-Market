import json

class JsServerProduct:
    __PATH = "DataServer\\repository\\products.json"

    @classmethod
    def __pull(cls):
        try:
            with open(cls.__PATH, "r") as js:
                data = json.load(js)
        except:
            raise Exception("Error [Product data service]:  Pull data is not possible.")
        else:
            return data

    @classmethod
    def requestForGetAListOfProducs(cls, category):
        data = cls.__pull()
        try:
            target = data[category]
        except:
            raise Exception("Error [Product data service]: The category is not found.")
        else:
            return target

    @classmethod
    def requestForGetAProduct(cls, category, product):
        category_data = cls.requestForGetAListOfProducs(category)
        try:
            target = category_data[product]
        except:
            raise Exception("Error [Product data service]: The product is not found.")
        else:
            return target

    @classmethod
    def requestForGetAListOfCategories(cls):
        data = cls.__pull()
        return list(data.keys())

    @classmethod
    def requestForUpdateTheValueOfAkey(cls, category, product_code, key, value):
        data = cls.__pull()
        try:
            data[category][product_code][key] = value
        except:
            if category not in data:
                raise Exception("Error [Product data service]: updating the value of a key is not possible. category id not found.")
            elif product not in data[category]:
                raise Exception("Error [Product data service]: updating the value of a key is not possible. product not found.")
            else:
                raise Exception("Error [Product data service]: updating the value of a key is not possible. key not found.")
        else:
            with open(cls.__PATH, "w") as Js:
                json.dump(data, Js, indent=4)
