import httprequests

url = 'https://admin:admin@127.0.0.1:5000/hosts/host1'
putdata = {'ip': '99.99.99.99', 'rectype' : 'A'}
scode = httprequests.httpPut(url,putdata)
print scode
