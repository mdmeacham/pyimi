name = "pyimi"

import sys

#if sys.version_info.major < 3:
#    print("Must be run with Python 3")
#    sys.exit(1)

from .imi import IMI
from .exceptions import IMIAuthError, IMIConnectionError, MoveError, CreateError
from .directories import Directories, Directory
from .devices import Devices, Device
from .profiles import Profiles, Profile
from .assets import Assets, Asset