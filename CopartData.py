class Copart:
    def __init__(self, stockNum, auctionDate, year, tranny, model, loc):
        self.stockNum = stockNum
        self.auctionDate = auctionDate
        self.year = year
        self.tranny = tranny
        self.model = model
        self.loc = loc

    def toString(self):
        return "Stock #: " + self.stockNum + ", Year: " + str(self.year) + ", Tranny: " + self.tranny + ", Model: " + self.model + ", Auction Date: " + self.auctionDate + ", Location: " + self.loc