import requests
from requests.auth import HTTPBasicAuth
import json

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
        self.url_host_port = 'https://' + server + ':' + str(port)
        self.headers = {'content-type': 'application/json'}
        self.headers['Cookie'] = self.make_request(requests.post, end_of_url='/umsapi/v3/login', auth=HTTPBasicAuth(user, password))['message']

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
    
    def request_info(self, id, detailed=False, check_status=False):
        query = ''
        if detailed:
            query = '?facets=details'
        elif check_status:
            query = '?facets=online'

        url_string = '/umsapi/v3/thinclients/{id}{query}'.format(id=str(id), query=query)
        return self.make_request(requests.get, end_of_url=url_string)
