
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


class Candles:
    def __init__(self, candle_info):
        self.close = float(candle_info['close'])
        self.high = float(candle_info['high'])
        self.low = float(candle_info['low'])
        self.open = float(candle_info['open'])
        self.time = candle_info['time']
        self.volume = candle_info['volume']


class OrderStatus:
    def __init__(self, order_info):
        self.orderUuid = order_info['orderUuid']
        self.order_type = order_info['order_type']
        self.primary_asset = order_info['primary_asset']
        self.secondary_asset = order_info['secondary_asset']
        self.quantity_asset = order_info['quantity_asset']
        self.quantity = order_info['quantity']
        self.trigger = order_info['trigger']
        self.status = order_info['status']
        self.created_time = order_info['created_time']
        self.updated_time = order_info['updated_time']
        self.amount = order_info['amount']
        self.total = order_info['total']
        self.rate = order_info['rate']
        self.audValue = order_info['audValue']
        self.feeAmount = order_info['feeAmount']
        self.feeAsset = order_info['feeAsset']
        self.feeAudValue = order_info['feeAudValue']