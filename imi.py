import requests
from requests.auth import HTTPBasicAuth
import json

requests.packages.urllib3.disable_warnings()

class Directory:
    def __init__(self, imi_data, imi):
        self.id = imi_data['id']
        self.name = imi_data['name']
        self.parent_id = imi_data['parentID']

class Device:
    def __init__(self, imi_data, imi):
        self.id = imi_data['id']
        self.name = imi_data['name']
        self.ip = imi_data['lastIP']
        self.mac = imi_data['mac']
        self.info = None
        self.detailed_retrieved = False
        self.imi = imi

    def get_info(self, detailed=False):
        if self.info == None or (detailed == True and self.detailed_retrieved == False):
            self.info = self.imi.request_info(self.id, detailed)
            if detailed:
                self.detailed_retrieved = True
    
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

class Devices:
    def __init__(self, imi, filter=None):
        self.imi = imi
        self.devices = []
        for item in self.imi.request_devices():
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

class Directories:
    def __init__(self, imi, filter=None):
        self.imi = imi
        self.directories = []
        for item in self.imi.request_directories():
            self.directories.append(Directory(item, self.imi))

    def __iter__(self):
        return iter(self.directories)
    
    def __getitem__(self, index):
        return self.directories[index]

    def find(self, name=None):
        if name:
            return [directory for directory in self.directories if directory.name == name][0]

class IMI:
    def __init__(
            self,
            server = None, 
            port = 8443, 
            verify = False,
            user = None,
            password = None):

        self.verify = verify
        self.url_host_port = 'https://' + server + ':' + str(port)
        self.headers = {'content-type': 'application/json'}
        self.session_id = self.make_request(requests.post, end_of_url='/umsapi/v3/login', auth=HTTPBasicAuth(user, password))['message']
        self.headers = {'Cookie': self.session_id, 'content-type': 'application/json'}

    def make_request(self, requests_method=None, data=None, end_of_url=None, auth=None):
        url_string = self.url_host_port + end_of_url
        response = requests_method(url_string, verify=self.verify, data=json.dumps(data), headers=self.headers, auth=auth)
        return response.json()        
    
    def request_command(self, command, device_id):
        url_string = '/umsapi/v3/thinclients?command={command}'.format(command=command)
        data = [{"id": str(device_id), "type": "tc"}]
        return self.make_request(requests.post, data=data, end_of_url=url_string)

    def request_move(self, directory_id, device_id):
        url_string = '/umsapi/v3/directories/tcdirectories/{id}?operation=move'.format(id=str(directory_id))
        data = [{"id": str(device_id), "type": "tc"}]
        return self.make_request(requests.put, data=data, end_of_url=url_string)

    def request_devices(self):
        return self.make_request(requests.get, end_of_url='/umsapi/v3/thinclients')

    def request_directories(self):
        return self.make_request(requests.get, end_of_url='/umsapi/v3/directories/tcdirectories')
    
    def request_info(self, id, detailed=False):
        url_string = '/umsapi/v3/thinclients/{id}{query}'.format(id=str(id), 
            query='?facets=details' if detailed else '')
        return self.make_request(requests.get, end_of_url=url_string)

if __name__ == '__main__':
    imi = IMI(server='192.168.56.12', user='igel', password='igel123')
    devices = Devices(imi)
    directories = Directories(imi)

    for device in devices:
        print(device.name)
    
    for directory in directories:
        print(directory.name)
    

    found_device = devices.find(name="ITC080027B8A48E")
    if found_device.name == "ITC080027B8A48E":
        print("found device worked!")
    #found_device = devices.find(name="ITC080027B8A48E")
    #found_device = devices.find(ip="192.168.56.101")
    #found_device = devices.find(mac="080027B8A48E")
    #print("found ", found_device.name)

    found_directory = directories.find(name="Portland")
    if found_directory.name == "Portland":
        print("found directory worked!")

    found_device.move(found_directory)
    found_device.get_info()
    if found_device.info['parentID'] == '224':
        print("Move to directory worked!")
    
    print("Before detailed retrieve, found device info is: ", found_device.info)

    found_device.get_info(detailed=True)
    
    print("After detailed retrieve, found device info is: ", found_device.info)

    found_device.reboot()

    
    

