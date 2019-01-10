# flake8: noqa
from pedialabsnew.settings_shared import *

try:
    from pedialabsnew.local_settings import *
except ImportError:
    pass
