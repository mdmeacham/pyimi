from .exceptions import MoveError
from .assets import Asset

class Device:
    def __init__(self, imi_data, imi):
        self.id = imi_data['id']
        self.name = imi_data['name']
        self.ip = imi_data['lastIP']
        self.mac = imi_data['mac']
        self.info = None
        self.detailed_retrieved = False
        self.imi = imi
        self._online = False

    def get_info(self, detailed=False):
        if self.info == None or (detailed == True and self.detailed_retrieved == False):
            self.info = self.imi.request_info(self.id, detailed)
            if detailed:
                self.detailed_retrieved = True
    
    @property
    def online(self):
        self._check_status()
        return self._online

    def _check_status(self):
        self._online = self.imi.request_info(self.id, check_status=True)['online']
    
    @property
    def assets(self):
        self._get_assets()
        return self._assets

    def _get_assets(self):
        assets = self.imi.request_tc_asset_info(self.id)['assetinfos']
        self._assets = []
        for asset in assets:
            self._assets.append(Asset(asset, self.imi))

    def reboot(self):
        return self.imi.request_command('reboot', self.id)
    
    def factory(self):
        return self.imi.request_command('tcreset2facdefs', self.id)
        
    def shutdown(self):
        return self.imi.request_command('shutdown', self.id)

    def wakeup(self):
        return self.imi.request_command('wakeup', self.id)

    def settings2tc(self):
        return self.imi.request_command('settings2tc', self.id)
    
    def move(self, directory):
        if not directory:
            raise MoveError('Unable to move device into invalid directory')
        try:
            return self.imi.request_move(directory.id, self)
        except:
            raise MoveError('Unable to move device')

    def assign(self, profile):
        return self.imi.assign_unassign_profile('assign', profile.id, self)

    def unassign(self, profile):
        return self.imi.assign_unassign_profile('unassign', profile.id, self)

class Devices:
    def __init__(self, imi, filter=None):
        self.imi = imi
        self.devices = []
        for item in self.imi.request_items(end_of_url='thinclients/'):
            self.devices.append(Device(item, self.imi))
    
    def __iter__(self):
        return iter(self.devices)
    
    def __getitem__(self, index):
        return self.devices[index]
    
    def find(self, name=None, ip=None, mac=None, id=None):
        if name:
            key = 'name'
            value = name
        elif ip:
            key = 'ip'
            value = ip
        elif mac:
            key = 'mac'
            value = mac
        elif id:
            key = 'id'
            value = id
        try:
            return [device for device in self.devices if getattr(device, key) == value][0]
        except:
            return None
