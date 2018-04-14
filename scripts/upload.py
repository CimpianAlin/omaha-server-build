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
from uuid import uuid4
import sys
import json
import os
from distutils.version import StrictVersion

host = 'web'
username = 'admin'
password = 'admin'
uuid = ""

dsa_signature = os.environ.get('DSA_SIGNATURE')
if not dsa_signature:
	raise UserWarning("No environment variable DSA_SIGNATURE found")

path = sys.argv[1]
if not path:
	raise UserWarning("Usage: {} <path_to_upload>".format(sys.argv[0]))

name = os.path.basename(path)

url = 'http://{}/api/app/'.format(host)
print('[INFO] Making request to {}'.format(url))
r = requests.get(url, auth=HTTPBasicAuth(username, password))
if not r.ok:
	print(r.text)
	raise UserWarning("{} response from {} to {}".format(r.status_code, r.request.method, r.request.url))

apps = json.loads(r.text)
app = [app for app in apps if app['name'] == 'test']
if app:
	app = app[0]
	print("Found: {}".format(app['name']))
	uuid = app['id']
else:
	uuid = str(uuid4())
	data = MultipartEncoder(
		fields=dict(
			id=uuid,
			name='test'
		)
	)

	r = requests.post(url, data=data, auth=HTTPBasicAuth(username, password), headers={'Content-Type': data.content_type})
	if not r.ok:
		print(r.text)
		raise UserWarning("{} response from {} to {}".format(r.status_code, r.request.method, r.request.url))

url = 'http://{}/api/sparkle/version/'.format(host)
r = requests.get(url, auth=HTTPBasicAuth(username, password))
if not r.ok:
	print(r.text)
	raise UserWarning("{} response from {} to {}".format(r.status_code, r.request.method, r.request.url))

try:
	versions = [x['version'] for x in json.loads(r.text)]
	current_ver = sorted(versions, key=StrictVersion)[-1]

except IndexError:
	current_ver = "1.0"

minor_ver = current_ver.split('.')[-1]
upload_ver = current_ver.split('.')
upload_ver[-1] = str(int(current_ver.split('.')[-1]) + 1)
upload_ver = '.'.join(upload_ver)


path_to_new_version_file = sys.argv[1]
data = MultipartEncoder(
	fields=dict(
	    app=uuid,
	    channel='1',
	    version=upload_ver,
	    short_version=upload_ver,
	    dsa_signature=dsa_signature,
	    file=(name, open(path, 'rb'), 'text/plain'),
	)
)
r = requests.post(url, data=data, auth=HTTPBasicAuth(username, password), headers={'Content-Type': data.content_type})

if not r.ok:
	print(r.text)
	raise UserWarning("{} response from {} to {}".format(r.status_code, r.request.method, r.request.url))

print(r.text)
