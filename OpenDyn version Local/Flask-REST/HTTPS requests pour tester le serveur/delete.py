import httprequests

url = 'https://admin:admin@127.0.0.1:5000/hosts/toto'
scode = httprequests.httpDelete(url)
print scode
