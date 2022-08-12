class Beer:
    price = 25
    def __init__(self, price):
        self.price = 2
        self.price2 = price
        print("__init__")
    
    def printAgePriv(self):
        print(self.age2)

    @classmethod
    def newBeerPromotion(cls, price, promotion):
        cls.priceTEST = 19
        return cls(price-promotion)
 
    @staticmethod
    def printAgeStatic():
        print("static method")



beer = Beer.newBeerPromotion(20, 10)
print(beer.price2)

beer2 = Beer(20)
print(beer2.price)

# __class__ pozwala odnieść się do zmiennych które nie są w konstruktorze(te które mają selfa czyli te króre są tworzone dopiero przy tworzeniu instancji, atrubuty obiektu) 
# są to zmienne nalerzące do klasy, mamy do nich dostęp nawet przed uworzeniem instancji danej klasy

print(beer2.__class__.__name__)
print(beer2.price2)
