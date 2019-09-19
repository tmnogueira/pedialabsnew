# flake8: noqa
from pedialabsnew.settings_shared import *
from ccnmtlsettings.production import common

locals().update(
    common(
        project=project,
        base=base,
        STATIC_ROOT=STATIC_ROOT,
        INSTALLED_APPS=INSTALLED_APPS,
        cloudfront="d7uu01oz70ieq",
    )
)

try:
    from pedialabsnew.local_settings import *
except ImportError:
    pass
