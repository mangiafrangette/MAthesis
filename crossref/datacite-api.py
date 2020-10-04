import requests 
# eventually  add this: from requests.auth import HTTPBasicAuth
# eventually add this to the requests.get argument after url: auth=HTTPBasicAuth('user', 'pass')


url = "https://api.test.datacite.org/dois/10.16995/dm.75"
# payload = {'some': 'data'}
r = requests.get(url)
r.json()

with open("datacite-api.json", "wb") as fd:
  for chunk in r.iter_content():
    fd.write(chunk) 
