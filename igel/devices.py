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
        return self.imi.request_move(directory.id, self.id)

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
    
    def find(self, name=None, ip=None, mac=None):
        if name:
            return [device for device in self.devices if device.name == name][0]
        if ip:
            return [device for device in self.devices if device.ip == ip][0]
        if mac:
            return [device for device in self.devices if device.mac == mac][0]
