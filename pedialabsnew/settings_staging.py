# flake8: noqa
from pedialabsnew.settings_shared import *
from ccnmtlsettings.staging import common

locals().update(
    common(
        project=project,
        base=base,
        STATIC_ROOT=STATIC_ROOT,
        INSTALLED_APPS=INSTALLED_APPS,
        cloudfront="d2abdva9k9ectf",
    )
)

try:
    from pedialabsnew.local_settings import *
except ImportError:
    pass
