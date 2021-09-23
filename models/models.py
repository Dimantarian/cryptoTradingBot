
# [
#   {
#     "assetId": 1,
#     "availableBalance": "100.2464"
#   }
# ]


class Asset:
    def __init__(self, asset_info):
        self.symbol = asset_info['code']
        self.assetId = asset_info['id']
        self.name = asset_info['name']


class Balance:
    def __init__(self, balance_info):
        self.symbol = balance_info['symbol']
        self.assetId = balance_info['assetId']
        self.balance = balance_info['availableBalance']