
'''
# Post
url = 'https://admin:admin@127.0.0.1:5000/hosts'
putdata = {'ip': '33.33.33.50', 'hostname' : 'fuckface', 'rectype' :'A'}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post(url, data=json.dumps(putdata), headers=headers, verify=False)
'''

import httprequests

url = 'https://admin:admin@127.0.0.1:5000/hosts'
putdata = {'ip': '33.33.33.50', 'hostname' : 'toto', 'rectype' :'A'}

scode = httprequests.httpPost(url, putdata)

print scode



