import requests
from requests.auth import HTTPBasicAuth
import json
from .directories import Directory
from .devices import Device

requests.packages.urllib3.disable_warnings()

class IMI:
    def __init__(
            self,
            server = None, 
            port = 8443, 
            verify = False,
            user = None,
            password = None):

        self.verify = verify
        self.url = 'https://{server}:{port}/umsapi/v3/'.format(server=server, port=str(port))
        self.headers = {'content-type': 'application/json'}
        self.headers['Cookie'] = self.make_request(requests.post, end_of_url='login', auth=HTTPBasicAuth(user, password))['message']

    def make_request(self, requests_method=None, data=None, end_of_url=None, auth=None):
        url = '{url}{end}'.format(url=self.url, end=end_of_url)
        response = requests_method(url, verify=self.verify, data=json.dumps(data), headers=self.headers, auth=auth)
        return response.json()        
    
    def request_command(self, command, device_id):
        end_of_url = 'thinclients?command={command}'.format(command=command)
        data = [{"id": str(device_id), "type": "tc"}]
        return self.make_request(requests.post, data=data, end_of_url=end_of_url)

    def request_move(self, directory_id, device_id):
        end_of_url = 'tcdirectories/{id}?operation=move'.format(id=str(directory_id))
        data = [{"id": str(device_id), "type": "tc"}]
        return self.make_request(requests.put, data=data, end_of_url=end_of_url)

    def assign_unassign_profile(self, operation=None, profile_id=None, to=None):
        if isinstance(to, Directory):
            to_str = 'tcdirectories'
            to_type = 'tcdirectory'
        elif isinstance(to, Device):
            to_str = 'thinclients'
            to_type = 'tc'
        end_of_url = 'profiles/{id}/assignments/{to}/'.format(id=str(profile_id), to=to_str)
        if operation == 'assign':
            end_of_url = 'profiles/{id}/assignments/{to}/'.format(id=str(profile_id), to=to_str)
            data = [{"assignee": {"id": str(profile_id), "type": "profile"}, "receiver": {"id": str(to.id), "type": to_type}}]
            return self.make_request(requests.put, data=data, end_of_url=end_of_url)
        else:
            end_of_url = 'profiles/{id}/assignments/{to}/{to_id}'.format(id=str(profile_id), to=to_str, to_id=str(to.id))
            return self.make_request(requests.delete, end_of_url=end_of_url)

    def request_items(self, end_of_url=None):
        return self.make_request(requests.get, end_of_url=end_of_url)
    
    def request_info(self, id, detailed=False, check_status=False):
        query = ''
        if detailed:
            query = '?facets=details'
        elif check_status:
            query = '?facets=online'

        end_of_url = 'thinclients/{id}{query}'.format(id=str(id), query=query)
        return self.make_request(requests.get, end_of_url=end_of_url)
