import requests
import json

'''
Basic http methodes by JSON header, returns status code
'''

#the header for JSON
JSON_HEADER = {'Content-type': 'application/json', 'Accept': 'text/plain'}

# POST
def httpPost(url, putdata):
	r = requests.post(url, data=json.dumps(putdata), headers=JSON_HEADER, verify=False)
	return r.status_code

# PUT
def httpPut(url, putdata):
	r = requests.put(url, data=json.dumps(putdata), headers=JSON_HEADER, verify=False)
	return r.status_code

# DELETE
def httpDelete(url):
	r = requests.delete(url, verify = False)
	return r.status_code
	


'''
Example usage : 
	- please use the correct URL on REST server!! 

POST	: adds a new host called "toto" on the server
	>>> url = 'https://admin:admin@127.0.0.1:5000/hosts'
	>>> putdata = {'ip': '33.33.33.50', 'hostname' : 'toto', 'rectype' :'A'}
	>>> scode = httprequests.httpPost(url,putdata)
	>>> print(scode)

PUT	: updates the information of "host1" on the server
	>>> url = 'https://admin:admin@127.0.0.1:5000/hosts/host1'
	>>> putdata = {'ip': '99.99.99.99', 'rectype' : 'A'}
	>>> scode = httprequests.httpPut(url,putdata)
	>>> print(scode)

DELETE	: deletes a host called "toto" on the server
	>>> url = 'https://admin:admin@127.0.0.1:5000/hosts/toto'
	>>> scode = httprequests.httpDelete(url)
	>>> print(scode)

'''
