from .exceptions import MoveError, CreateError


class Directory:
    def __init__(self, imi_data, imi):
        self._imi = imi
        self.id = imi_data['id']
        self.name = imi_data['name']
        self.parent_id = imi_data['parentID']

    def assign(self, profile):
        end_of_url = 'profiles/{id}/assignments/tcdirectories/'.format(id=str(profile.id))
        data = [{"assignee": {"id": str(profile.id), "type": "profile"}, "receiver": {"id": str(self.id), "type": "tcdirectory"}}]
        return self._imi.make_request('put', data=data, end_of_url=end_of_url)

    def unassign(self, profile):
        end_of_url = 'profiles/{id}/assignments/tcdirectories/{to_id}'.format(id=str(profile.id), to_id=str(self.id))
        return self._imi.make_request('delete', end_of_url=end_of_url)

    def move(self, directory):
        if not directory:
            raise MoveError('Unable to move directory into invalid directory')
        try:
            end_of_url = 'directories/tcdirectories/{id}?operation=move'.format(id=str(directory.id))
            data = [{"id": str(self.id), "type": "tcdirectory"}]
            return self._imi.make_request(method='put', data=data, end_of_url=end_of_url)
        except:
            raise MoveError('Unable to move directory')

class Directories:
    def __init__(self, imi, filter=None):
        self._imi = imi
        self.directories = []
        for item in self._imi.make_request(method='get', end_of_url='directories/tcdirectories/'):
            self.directories.append(Directory(item, self._imi))

    def create(self, name=None):
        if not name:
            raise CreateError("Must provide name of object to create")
        try:
            end_of_url = 'directories/tcdirectories/'
            data = {"name": name}
            return self._imi.make_request(method='put', data=data, end_of_url=end_of_url)
        except:
            raise CreateError("Unable to create new object")

    def __iter__(self):
        return iter(self.directories)
    
    def __getitem__(self, index):
        return self.directories[index]

    def find(self, name=None, id=None):
        if name:
            key = 'name'
            value = name
        elif id:
            key = 'id'
            value = id
        else:
            return None
        try:
            return [directory for directory in self.directories if getattr(directory, key) == value][0]
        except:
            return None
