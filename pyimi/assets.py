from .exceptions import MoveError
from datetime import datetime

class Asset:
    def __init__(self, imi_data, imi):
        self._imi = imi
        self.id = imi_data['assetId']
        self.name = imi_data['assetName']
        self.vendor_id = imi_data['assetVendor']
        self.product_id = imi_data['deviceId']
        self.connector = imi_data['connector']

    @property
    def info(self):
        self._get_info()
        return self._info

    def _get_info(self):
        end_of_url = 'assetinfo/assets/{id}'.format(id=str(self.id))
        self._info = self._imi.make_request(method='get', end_of_url=end_of_url)

    @property
    def history(self):
        self._get_history()
        return self._history

    def _get_history(self):
        end_of_url = 'assethistory/assets/{id}'.format(id=str(self.id))
        self._history = self._imi.make_request(method='get', end_of_url=end_of_url)['assethistories']
        for history in self._history:
            time_str = str(history['eventTimeStamp'])[:10]
            time_int = int(time_str)
            history['ctime'] = datetime.fromtimestamp(time_int).ctime()

class Assets:
    def __init__(self, imi, filter=None):
        self._imi = imi
        self.assets = []
        results = self._imi.make_request(method='get', end_of_url='assetinfo/')['assetinfos']
        for item in results:
            do_not_add = False
            # Do not add if it's a duplicate product id
            for asset in self.assets:
                if asset.vendor_id == item['assetVendor'] and asset.product_id == item['deviceId']:
                    do_not_add = True
            if not do_not_add:
                self.assets.append(Asset(item, self._imi))

    def __iter__(self):
        return iter(self.assets)
   
    def __getitem__(self, index):
        return self.assets[index]