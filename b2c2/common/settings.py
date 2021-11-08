# -*- coding: utf-8 -*-
import os

from dotenv import dotenv_values, load_dotenv

load_dotenv()
config = {
    **dotenv_values(".env"),  # load shared development variables
    **os.environ,  # override loaded values with environment variables
}

REMOTE_API_URL = "https://api.uat.b2c2.net"
LOCAL_API_URL = "http://127.0.0.1:8000"

if config.get("LOCAL"):
    API_URL = LOCAL_API_URL
else:
    API_URL = REMOTE_API_URL
