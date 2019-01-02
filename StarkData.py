class Stark:
    
    def __init__(self, stockNum, year, tranny):
        self.stockNum = stockNum
        self.year = year
        self.tranny = "" if tranny is None else tranny

    def print(self):
        print("Stock #:",self.stockNum,", Year:",self.year,", Tranny:",self.tranny)
