import httprequests

url = 'https://admin:admin@127.0.0.1:5000/hosts'
putdata = {'ip': '33.33.33.50', 'hostname' : 'toto', 'rectype' :'A'}

scode = httprequests.httpPost(url, putdata)

print scode



