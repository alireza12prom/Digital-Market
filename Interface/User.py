from abc import ABC, abstractmethod


class UserInterface(ABC):
    
    @abstractmethod
    def profile(self):
        pass

    @abstractmethod
    def myShoppingBag(self):
        pass

    @abstractmethod
    def myFavoriteProducts(self):
        pass

    @abstractmethod
    def myShoppingHistory(self):
        pass

    @abstractmethod
    def categories(self):
        pass

    @abstractmethod
    def products(self):
        pass

    @abstractmethod
    def addAProductToMyFavorites(self):
        pass

    @abstractmethod
    def removeAProductFromMyFavorites(self):
        pass

    @abstractmethod
    def addAProductToMyShoppingBag(self):
        pass

    @abstractmethod
    def removeAProductFromMyShoppingBag(self):
        pass

    @abstractmethod
    def confirmOrder(self):
        pass
    
    @abstractmethod
    def cancelOrder(self):
        pass
    
    @abstractmethod
    def clearHistory(self):
        pass