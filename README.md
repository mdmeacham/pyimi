A python library for accessing IGEL's IMI

``` {.sourceCode .python}
from imi import IMI, Devices, Directories

# First, create your IMI session
imi = IMI(server='192.168.56.12', user='igel', password='igel123')

# retrieve a list of your devices
devices = Devices(imi)

# and also a list of your directories
directories = Directories(imi)

# you can iterate through the devices and directories
for device in devices:
    print(device.name)

for directory in directories:
    print(directory.name)

# Or, to find pa paricular device, you can search
# by name, IP address, or MAC
device1 = devices.find(name="ITC080027B8A48E")
device2 = devices.find(ip="192.168.56.101")
device3 = devices.find(mac="080027B8A48E")
device3.name

# You can find a directory by name
my_directory = directories.find(name="Portland")
my_directory.name

# Now that you have both a device and a directory,
# you can move the device into that directory
device1.move(my_directory)

# Get some additional information about your device
device1.get_info()
device1.info

# Get more detailed information
device1.get_info(detailed=True)
# Now, device info shows more
device1.info

# Run some command on your device
device1.reboot()
device1.shutdown()
device1.wakeup()
device1.settings2tc()
device1.factory()

# For now, when you factory a device
# you should retrieve all devices again to have a
# valid list

```