from .base import *  # noqa

DEVELOPMENT_APPS = [
    'debug_toolbar',
]

INTERNAL_IPS = [
    "127.0.0.1",
]

INSTALLED_APPS += DEVELOPMENT_APPS  # noqa: F405

MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware') # noqa: F405