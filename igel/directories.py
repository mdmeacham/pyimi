class Directory:
    def __init__(self, imi_data, imi):
        self.imi = imi
        self.id = imi_data['id']
        self.name = imi_data['name']
        self.parent_id = imi_data['parentID']

    def assign(self, profile):
        return self.imi.assign_unassign_profile('assign', profile.id, self)

    def unassign(self, profile):
        return self.imi.assign_unassign_profile('unassign', profile.id, self)


class Directories:
    def __init__(self, imi, filter=None):
        self.imi = imi
        self.directories = []
        for item in self.imi.request_items(end_of_url='directories/tcdirectories/'):
            self.directories.append(Directory(item, self.imi))

    def __iter__(self):
        return iter(self.directories)
    
    def __getitem__(self, index):
        return self.directories[index]

    def find(self, name=None):
        if name:
            return [directory for directory in self.directories if directory.name == name][0]
