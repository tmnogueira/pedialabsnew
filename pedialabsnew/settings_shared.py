# Django settings for pedialabsnew project.
import os.path
from ccnmtlsettings.shared import common

import urllib3.contrib.pyopenssl

# Tell urllib3 to use pyOpenSSL. Needed by python < 2.7.9
# to resolve an SNIMissingWarning.
# See:
#   https://urllib3.readthedocs.io/en/latest/user-guide.html#ssl-py2
#   https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
urllib3.contrib.pyopenssl.inject_into_urllib3()

project = 'pedialabsnew'
base = os.path.dirname(__file__)

locals().update(common(project=project, base=base))

PROJECT_APPS = [
    'pedialabsnew.main',
    'pedialabsnew.exercises',
]

USE_TZ = True

TEMPLATES[0]['OPTIONS']['context_processors'].append(  # noqa
    'pedialabsnew.main.views.context_processor'
)

INSTALLED_APPS += [  # noqa
    'bootstrap3',
    'sorl.thumbnail',
    'bootstrapform',
    'django_extensions',
    'registration',
    'pagetree',
    'pageblocks',
    'quizblock',
    'pedialabsnew.main',
    'pedialabsnew.exercises',
    'pedialabsnew.rstplot',
]

PAGEBLOCKS = [
    'pageblocks.TextBlock',
    'pageblocks.HTMLBlock',
    'pageblocks.PullQuoteBlock',
    'pageblocks.ImageBlock',
    'pageblocks.ImagePullQuoteBlock',
    'quizblock.Quiz',
    'exercises.Lab',
    'rstplot.RstPlotBlock',
]

LETTUCE_APPS = (
    'pedialabsnew.main',
    'pedialabsnew.exercises',
)

ACCOUNT_ACTIVATION_DAYS = 7
