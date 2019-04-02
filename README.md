A python library for accessing IGEL's IMI

``` {.sourceCode .python}
from igel import IMI, Devices, Directories, Profiles

# First, create your IMI session
imi = IMI(server='192.168.56.12', user='igel', password='igel123')

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
# by name, IP address, or MAC
device1 = devices.find(name="ITC080027B8A48E")
device2 = devices.find(ip="192.168.56.104")
#device3 = devices.find(mac="080027B8A48E")
print("device1 IP address is", device1.ip)
print("device2 name is", device2.name)

# Check if your device is online like this
print("Is device1 online?", device1.online)
print("Is device2 online?", device2.online)

# You can find a directory by name
my_directory = directories.find(name="Portland")
print("my_directory name is", my_directory.name)

# Now that you have both a device and a directory,
# you can move the device into that directory
device1.move(my_directory)

# Get some additional information about your device
device1.get_info()
print("A smaller set of device info includes:", device1.info)

# Get more detailed information
device1.get_info(detailed=True)
# Now, device info shows more
print("A much larger set of device info includes:", device1.info)

# Run some commands on your device
device1.reboot()
device1.shutdown()
device1.wakeup()
device1.settings2tc()
#device1.factory()

# For now, when you factory a device
# you should retrieve all devices again to have a
# valid list
```