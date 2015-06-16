__author__ = 'jiaying.lu'

__all__ = ["LOGENTRIES_TOKEN", "BUGSNAG_TOKEN", "APP_ENV"]
import os

# Settings

LOGENTRIES_DEV_TOKEN = "3f234d7c-e085-433e-b561-43d06e2a7d72"
LOGENTRIES_PROD_TOKEN = "01be0eb7-77c7-4c56-a1e3-1f87378271f1"
LOGENTRIES_LOCAL_TOKEN = "3f234d7c-e085-433e-b561-43d06e2a7d72"

BUGSNAG_DEV_TOKEN = "6565edbfe11d97625383c260a8764e0f"
BUGSNAG_PROD_TOKEN = "1b9d9d38d627bd5ee4bf2409067ebcca"
BUGSNAG_LOCAL_TOKEN = "6565edbfe11d97625383c260a8764e0f"

LOGENTRIES_TOKEN = ""
BUGSNAG_TOKEN = ""
APP_ENV = ""

# Configuration

try:
    APP_ENV = os.environ["APP_ENV"]
except KeyError, key:
    print "KeyError: There is no env var named %s" % key
    print "The local env will be applied"
    APP_ENV = "local"
finally:
    if APP_ENV == "dev":
        LOGENTRIES_TOKEN = LOGENTRIES_DEV_TOKEN
        BUGSNAG_TOKEN = BUGSNAG_DEV_TOKEN
    elif APP_ENV == "prod":
        LOGENTRIES_TOKEN = LOGENTRIES_PROD_TOKEN
        BUGSNAG_TOKEN = BUGSNAG_PROD_TOKEN
    elif APP_ENV == "local":
        LOGENTRIES_TOKEN = LOGENTRIES_LOCAL_TOKEN
        BUGSNAG_TOKEN = BUGSNAG_LOCAL_TOKEN
