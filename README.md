# pyimi

pyimi is an **unsupported**, yet useful, python library for accessing IGEL's IMI.

### Overview

- Query for information about your IGEL endpoints
- Take actions such as reboot, shutdown, wakeup, send UMS settings and factory reset
- Assign profiles, move devices, create directories
- Query for asset inventory information (peripherals attached to the endpoints USB or bluetooth interface)

### Dependencies

pyimi depends on the Python requests library:

- [Python Requests] - Requests is an elegant and simple HTTP library for Python, built for human beings.

### Installation

Install the requests library like this.

```sh
$ pip install requests
```

Next, install pyimi itself like this

```sh
$ pip install pyimi
```

### Some example code

```python
from pyimi import IMI, Devices, Directories, Profiles, Assets
# First, create your IMI session
imi = IMI(server='192.168.56.12', user='igel', password='igel#123')

# retrieve a list of your devices
devices = Devices(imi)

# and also a list of your directories
directories = Directories(imi)

# and also a list of your Profiles
profiles = Profiles(imi)

# you can iterate through the retreived items
for device in devices:
    print(device.name)

for directory in directories:
    print(directory.name)

for profile in profiles:
    print(profile.name)

# Or, to find a paricular device, you can search
# by name, IP address, or MAC, or UMS assigned id
device1 = devices.find(name="ITC080027B8A48E")
device2 = devices.find(ip="192.168.56.104")
device3 = devices.find(mac="080027B8A48E")
device4 = devices.find(id="35591")

if device1:
    print("device1 IP address is", device1.ip)

if device2:
    print("device2 name is", device2.name)

# You can also filter the device list to return a
# sub list of devices whose info property has a
# matching key/value to the filter.
# Note: to find the possible keys for filter, check
# the dictionary returned by the device info property.
filtered_devices = devices.filter("site", "Downtown")
for device in filtered_devices:
    print(device.name)

# Check if your device is online like this
print("Is device1 online?", device1.online)
print("Is device2 online?", device2.online)

# Check when the device last contacted UMS
print("device1 contacted UMS at", device1.lastContact)

# You can find a directory by name
my_directory = directories.find(name="Portland")
if my_directory:
    print("Found directory")
else:
    print("directory was not found")

# Create a new directory for devices like this
directories.create("Vancouver")
# update the directories variable since there's a new dirctory
directories = Directories(imi)

# Now that you have both a device and a directory,
# you can move the device into that directory
device1.move(my_directory)

# And you can also move a device directory into another directory
my_directory2 = directories.find(name="Bend")
my_directory2.move(my_directory)

# Here's how you assign a profile to a device or a directory
browser_profile = profiles.find(name='Browser')
device1.assign(browser_profile)
my_directory.assign(browser_profile)

# And then you can unassign a profile like this
device1.unassign(browser_profile)
my_directory.unassign(browser_profile)


# Get some additional information about your device
print("Information about device:", device1.info)

# Run some commands on your device
device1.reboot()
device1.shutdown()
device1.wakeup()
device1.settings2tc()

# If this device has an EMP (Enterprise Mgmt Pack) license,
# query for it's Asset Inventory Tracker information.
device_assets = device1.assets
print("Assets for thin client", device1.name)
for asset in device1.assets:
    print("asset name:", asset.name, "asset id", asset.id)
    print("history of this asset on this device")
    for history in asset.history:
        print(history['ctime'], history, "\n")

# Factory reset a device
device1.factory()
# For now, when you factory a device
# you should retrieve all devices again to have a
# valid list

# retrieve a list of your assets through Asset Inventory Tracker
assets = Assets(imi)

# you can iterate through the retreived items
for asset in assets:
    print("Name of asset:", asset.name)
    print("Info about asset")
    for info in asset.info:
        print(info,"\n")
    print("History of asset")
    for history in asset.history:
        print(history['ctime'], history,"\n")
    print()

# Set extra information tags on your devices
device1.name = "IGEL-1"
device1.site = "Downtown"
device1.costCenter = "Anyone but us"
device1.comment = "no comment!!!"
device1.assetID = "123456789"
device1.inserviceDate = "01/21/20"
device1.serialNumber = "3495712"

print("Comment for this device", device1.comment)
print("Asset ID for this device", device1.assetID)
print("This device is located at", device1.site)
print("And this place paid for it", device1.costCenter)

# retrieve custom device attributes for a device
for attribute in device1.attributes:
    print(attribute['name'], ':', attribute['value'])


```

## License

MIT

[//]: # "These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax"
[python requests]: https://requests.readthedocs.io/en/master/
