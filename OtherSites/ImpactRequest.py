from datetime import datetime

class ImpactSearch:
    def __init__(self, model, year):
        self.AttributePageSize = 100
        self.AuctionMode = ""
        self.AuctionToday = False
        self.AuctionTomorrow = False
        self.BranchListPageIndex = 1
        self.IgnoreKeywordYear = False
        self.IsBuyNow = False
        self.IsBuyNowOffer = False
        self.IsKeywordSearch = True
        self.IsManagerPick = False
        self.IsNewSearch = True
        self.IsPreBidOutBid = False
        self.IsPreBidWinning = False
        self.IsVehicleRemarketing = False
        self.IsWatching = False
        self.Keyword = " "+ model.upper() +" "
        self.MakeListPageIndex = 1
        self.ModelListPageIndex = 1
        self.PageLoading = True
        self.RequestSource = ""
        self.RunlistPageIndex = 1
        self.RunlistPageSize = "100"
        self.RunlistSort = ""
        self.ShowOnlyPublicAuctions = False
        self.StockFilter = ""
        self.VehicleAge = "-1"
        self.VehicleBrand = ""
        self.VehicleTypeListPageIndex = 1
        self.YearFrom = "" if year is None else year
        self.YearTo = "" if year is None else str(datetime.now().year)
