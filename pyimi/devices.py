from .exceptions import MoveError
from .assets import Asset

class Device:
    def __init__(self, imi_data, imi):
        self.id = imi_data['id']
        self.name = imi_data['name']
        self.ip = imi_data['lastIP']
        self.mac = imi_data['mac']
        self.detailed_retrieved = False
        self._imi = imi
        self._info = None
        self._online = False

    @property
    def info(self):
        self._get_info()
        return self._info

    def _get_info(self):
        end_of_url = 'thinclients/{id}?facets=details'.format(id=str(self.id))
        self._info = self._imi.make_request(method='get', end_of_url=end_of_url)                

    @property
    def online(self):
        self._check_status()
        return self._online

    def _check_status(self):
        self._online = self._imi.request_info(self.id, check_status=True)['online']

    @property
    def assets(self):
        self._get_assets()
        return self._assets

    def _get_assets(self):
        end_of_url = 'assetinfo/thinclients/{id}'.format(id=str(self.id))
        assets = self._imi.make_request(method='get', end_of_url=end_of_url)['assetinfos']
        self._assets = []
        for asset in assets:
            self._assets.append(Asset(asset, self._imi))

    def _run_command(self, command):
        end_of_url = 'thinclients?command={command}'.format(command=command)
        data = [{"id": str(self.id), "type": "tc"}]
        return self._imi.make_request('post', data=data, end_of_url=end_of_url)

    def reboot(self):
        return self._run_command('reboot')

    def factory(self):
        return self._run_command('tcreset2facdefs')

    def shutdown(self):
        return self._run_command('shutdown')

    def wakeup(self):
        return self._run_command('wakeup')

    def settings2tc(self):
        return self._run_command('settings2tc')

    def move(self, directory):
        end_of_url = 'directories/tcdirectories/{id}?operation=move'.format(id=str(directory.id))
        data = [{"id": str(self.id), "type": "tc"}]
        if not directory:
            raise MoveError('Unable to move device into invalid directory')
        try:
            return self._imi.make_request('put', data=data, end_of_url=end_of_url)
        except:
            raise MoveError('Unable to move device')

    def assign(self, profile):
        end_of_url = 'profiles/{id}/assignments/thinclients/'.format(id=str(profile.id))
        data = [{"assignee": {"id": str(profile.id), "type": "profile"}, "receiver": {"id": str(self.id), "type": "tc"}}]
        return self._imi.make_request(method='put', data=data, end_of_url=end_of_url)

    def unassign(self, profile):
        end_of_url = 'profiles/{id}/assignments/thinclients/{to_id}'.format(id=str(profile.id), to_id=str(self.id))
        return self._imi.make_request(method='delete', end_of_url=end_of_url)

class Devices:
    def __init__(self, imi, filter=None):
        self._imi = imi
        self.devices = []
        for item in self._imi.make_request(method='get', end_of_url='thinclients/'):
            self.devices.append(Device(item, self._imi))

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
