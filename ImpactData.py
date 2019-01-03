class Impact:

    def __init__(self, stockNum, auctionDate, year, tranny, model):
        self.stockNum = stockNum
        self.auctionDate = auctionDate
        self.year = year
        self.tranny = tranny
        self.model = model

    def toString(self):
        return "Stock #: " + self.stockNum + ", Year: " + str(self.year) + ", Tranny: " + self.tranny + ", Model: " + self.model + ", Auction Date: " + self.auctionDate