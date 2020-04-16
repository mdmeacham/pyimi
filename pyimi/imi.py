import requests
from requests.auth import HTTPBasicAuth
import json
from .directories import Directory
from .devices import Device
from .exceptions import IMIAuthError, IMIConnectionError
import sys

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
        try:
            response = self.make_request(method='post', end_of_url='login', auth=HTTPBasicAuth(user, password))
            if response['message'].startswith('Invalid Login'):
                raise IMIAuthError('IMI Authorization failed')
            self.headers['Cookie'] = response['message']
        except IMIAuthError as err:
            raise err
        except:
            raise IMIConnectionError('Connection to IMI failed')

    def make_request(self, method=None, data=None, end_of_url=None, auth=None):
        if method == 'get':
            requests_method = requests.get
        elif method == 'post':
            requests_method = requests.post
        elif method == 'put':
            requests_method = requests.put
        elif method == 'delete':
            requests_method = requests.delete

        url = '{url}{end}'.format(url=self.url, end=end_of_url)
        response = requests_method(url, verify=self.verify, data=json.dumps(data), headers=self.headers, auth=auth)
        return response.json()        
'''    
    def request_command(self, command, device_id):
        end_of_url = 'thinclients?command={command}'.format(command=command)
        data = [{"id": str(device_id), "type": "tc"}]
        return self.make_request(requests.post, data=data, end_of_url=end_of_url)

    def request_move(self, directory_id, thing_to_move):
        end_of_url = 'directories/tcdirectories/{id}?operation=move'.format(id=str(directory_id))
        if isinstance(thing_to_move, Device):
            thing_type = "tc"
        elif isinstance(thing_to_move, Directory):
            thing_type = "tcdirectory"
        data = [{"id": str(thing_to_move.id), "type": thing_type}]
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
    
    def request_create(self, name=None):
        end_of_url = 'directories/tcdirectories/'
        data = {"name": name}
        return self.make_request(requests.put, data=data, end_of_url=end_of_url)
    
    def request_info(self, id, detailed=False, check_status=False):
        query = ''
        if detailed:
            query = '?facets=details'
        elif check_status:
            query = '?facets=online'

        end_of_url = 'thinclients/{id}{query}'.format(id=str(id), query=query)
        return self.make_request(requests.get, end_of_url=end_of_url)
    
    def request_asset_history(self, id):
        end_of_url = 'assethistory/assets/{id}'.format(id=str(id))
        return self.make_request(requests.get, end_of_url=end_of_url)

    def request_asset_info(self, id):
        end_of_url = 'assetinfo/assets/{id}'.format(id=str(id))
        return self.make_request(requests.get, end_of_url=end_of_url)

    def request_tc_asset_info(self, id):
        end_of_url = 'assetinfo/thinclients/{id}'.format(id=str(id))
        return self.make_request(requests.get, end_of_url=end_of_url)
'''