class Profile:
    def __init__(self, imi_data, imi):
        self.id = imi_data['id']
        self.name = imi_data['name']
        self._imi = imi

class Profiles:
    def __init__(self, imi, filter=None):
        self._imi = imi
        self.profiles = []
        for item in self._imi.make_request(method='get', end_of_url='profiles/'):
            self.profiles.append(Profile(item, self._imi))

    def __iter__(self):
        return iter(self.profiles)
    
    def __getitem__(self, index):
        return self.profiles[index]

    def find(self, name=None):
        if name:
            try:
                return [profile for profile in self.profiles if profile.name == name][0]
            except:
                return None
