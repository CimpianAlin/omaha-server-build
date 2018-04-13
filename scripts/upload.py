#!/usr/bin/env python
"""
requirements:
	- requests http://docs.python-requests.org/en/latest/
	- requests-toolbelt https://toolbelt.readthedocs.org/en/latest/
pip install requests requests-toolbelt
"""

import requests
from requests.auth import HTTPBasicAuth
from requests_toolbelt import MultipartEncoder
import sys
import json
import os


host = 'localhost'
username = 'admin'
password = 'admin'

#
# Upload New Sparkle Version
#

url = 'http://localhost:9090/api/sparkle/version/'
r = requests.get(url, auth=HTTPBasicAuth(username, password))
if r.status_code != 200:
	raise UserWarning("Non 200 response from {}".format(url))

try:
	current_ver = sorted(json.loads(r.text), key=lambda x: float(x['version']))[-1]['version']
except IndexError:
	current_ver = "1.0"

minor_ver = current_ver.split('.')[-1]
upload_ver = current_ver.split('.')
upload_ver[-1] = str(int(current_ver.split('.')[-1]) + 1)
upload_ver = '.'.join(upload_ver)


dsa_signature = os.environ.get('DSA_SIGNATURE')
if not dsa_signature:
    raise UserWarning("No DSA signature found in environment varirable DSA_SIGNATURE")

path_to_new_version_file = sys.argv[1]
data = MultipartEncoder(
	fields=dict(
	    app='1',
	    channel='1',
	    version=upload_ver,
	    short_version=upload_ver,
	    dsa_signature=dsa_signature,
	    file=(os.path.basename(sys.argv[1]), open(path_to_new_version_file, 'rb'), 'text/plain'),
	)
)
url = 'http://localhost:9090/api/sparkle/version/'
r = requests.post(
    url, data=data, auth=HTTPBasicAuth(username, password), headers={'Content-Type': data.content_type})

print(r.text)
