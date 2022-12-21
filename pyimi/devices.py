from .exceptions import MoveError
from .assets import Asset


class Device:
    def __init__(self, imi_data, imi):
        self.id = imi_data['id']
        self.unitid = imi_data['unitID']
        self._name = imi_data['name']
        self.ip = imi_data['lastIP']
        self.mac = imi_data['mac']
        self._imi = imi
        self._info = None
        self._attributes = None
        self._online = False

    @property
    def serialNumber(self):
        return self.info['serialNumber']

    @serialNumber.setter
    def serialNumber(self, serialNumber):
        data = {"serialNumber": serialNumber}
        self._set_tc_setting(data)

    @property
    def inserviceDate(self):
        return self.info['inserviceDate']

    @inserviceDate.setter
    def inserviceDate(self, inserviceDate):
        data = {"inserviceDate": inserviceDate}
        self._set_tc_setting(data)

    @property
    def assetID(self):
        return self.info['assetID']

    @assetID.setter
    def assetID(self, assetID):
        data = {"assetID": assetID}
        self._set_tc_setting(data)

    @property
    def comment(self):
        return self.info['comment']

    @comment.setter
    def comment(self, comment):
        data = {"comment": comment}
        self._set_tc_setting(data)

    @property
    def costCenter(self):
        return self.info['costCenter']

    @costCenter.setter
    def costCenter(self, costCenter):
        data = {"costCenter": costCenter}
        self._set_tc_setting(data)

    @property
    def department(self):
        return self.info['department']

    @department.setter
    def department(self, department):
        data = {"department": department}
        self._set_tc_setting(data)

    @property
    def site(self):
        return self.info['site']

    @site.setter
    def site(self, site):
        data = {"site": site}
        self._set_tc_setting(data)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        data = {"name": name}
        self._set_tc_setting(data)
        self._name = name

    def _set_tc_setting(self, data):
        end_of_url = '/thinclients/{id}'.format(id=str(self.id))
        result = self._imi.make_request(
            'put', data=data, end_of_url=end_of_url)
        print(result)

    @property
    def info(self):
        self._get_info()
        return self._info

    @property
    def attributes(self):
        self._get_attributes()
        return self._attributes

    @property
    def lastContact(self):
        return self.info['lastContact']

    def _get_info(self):
        end_of_url = 'thinclients/{id}?facets=details'.format(id=str(self.id))
        self._info = self._imi.make_request(
            method='get', end_of_url=end_of_url)

    def _get_attributes(self):
        end_of_url = 'thinclients/{id}?facets=deviceattributes'.format(
            id=str(self.id))
        self._attributes = self._imi.make_request(
            method='get', end_of_url=end_of_url)['deviceAttributes']

    @property
    def online(self):
        self._check_status()
        return self._online

    def _check_status(self):
        end_of_url = 'thinclients/{id}?facets=online'.format(
            id=str(self.id)
        )
        self._online = self._imi.make_request(
            method='get', end_of_url=end_of_url)['online']

    @property
    def assets(self):
        self._get_assets()
        return self._assets

    def _get_assets(self):
        end_of_url = 'assetinfo/thinclients/{id}'.format(id=str(self.id))
        assets = self._imi.make_request(
            method='get', end_of_url=end_of_url)['assetinfos']
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
        end_of_url = 'directories/tcdirectories/{id}?operation=move'.format(
            id=str(directory.id))
        data = [{"id": str(self.id), "type": "tc"}]
        if not directory:
            raise MoveError('Unable to move device into invalid directory')
        try:
            return self._imi.make_request('put', data=data, end_of_url=end_of_url)
        except:
            raise MoveError('Unable to move device')

    def assign(self, profile):
        end_of_url = 'profiles/{id}/assignments/thinclients/'.format(
            id=str(profile.id))
        data = [{"assignee": {"id": str(profile.id), "type": "profile"}, "receiver": {
            "id": str(self.id), "type": "tc"}}]
        return self._imi.make_request(method='put', data=data, end_of_url=end_of_url)

    def unassign(self, profile):
        end_of_url = 'profiles/{id}/assignments/thinclients/{to_id}'.format(
            id=str(profile.id), to_id=str(self.id))
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

    def find(self, name=None, ip=None, mac=None, id=None, unitid=None):
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
        elif unitid:
            key = 'unitid'
            value = unitid
        else:
            return None
        try:
            return [device for device in self.devices if getattr(device, key) == value][0]
        except:
            return None

    def filter(self, info_key, info_value):
        try:
            return [device for device in self.devices if device.info[info_key] == info_value]
        except:
            return None
