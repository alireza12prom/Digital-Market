class Category_iterator:
    def __init__(self, pages, pages_number):
        self.__pages = pages
        self.__pages_number = pages_number
        self.__current_page = self.__pages
        self.__current_page_number = 1
    
    @property
    def page_number(self):
        return "{} Of {}".format(self.__current_page_number, self.__pages_number)
     
    def currentPageData(self):
        if self.__current_page is None:
            return None
        else:
            return self.__current_page.data
    
    def next_page(self):
        if (self.__current_page is None) or (self.__current_page.next is None):
            return None
        else:
            self.__current_page = self.__current_page.next
            self.__current_page_number += 1
    
    def previous_page(self):
        if (self.__current_page is None) or (self.__current_page.previous is None):
            return None
        else:
            self.__current_page = self.__current_page.previous
            self.__current_page_number -= 1



class Page:
    def __init__(self, data):
        self.next = None
        self.data = data
        self.previous = None

class Category:
    """ 
    Evety category contans with a lot of pages.
    Every pages can only contains with 10 items.
    """
    def __init__(self):
        self.__pages = None
        self.__pages_number = 0

    # factory method
    def fromItems(self, items:dict):
        itemsOfAPage = dict()
        product_pages = [list(items.keys())[i:i+10] for i in range(0, len(items), 10)]
        for page in product_pages:
            for product_code in page:
                itemsOfAPage.update({product_code:items[product_code]})
            
            self.__insertANewPage(itemsOfAPage)
            self.__pages_number += 1
            itemsOfAPage = dict()
        return Category_iterator(self.__pages, self.__pages_number)
    
    def __insertANewPage(self, items:dict):
        newPage = Page(items)

        if self.__pages is None:
            self.__pages = newPage
        else:
            current_page = self.__pages
            while current_page.next:
                current_page = current_page.next

            current_page.next = newPage
            newPage.previous = current_page

