import requests
import urllib2
import json
import time
import socket
import sys


# need to put try/except statement for exceptions

# static variables and methodes
url = 'http://127.0.0.1:5000/hosts/host1'
monip = None

def checkValidIP(addr):
	try:
		print('Checking IP format.....')
		socket.inet_aton(addr)
		return True

	except socket.error:
		print("WRONG IP FORMAT")
		return False

# Obtenir l'adresse IP public de la machine a l'aide de plusieurs sites
# retourne l'adresse IP public si existe, retourne None sinon
def getPublicIP():
	# this way instead of loop on array because certain sites use different formats(requests,urllib etc)

	try:
		testip = urllib2.urlopen('http://ip.42.pl/raw').read()
		if checkValidIP(testip):
			return testip

		# 1st try
		testip = urllib2.urlopen('http://ip.42.pl/raw').read()
		if checkValidIP(testip):
			return testip

				
		# 2nd try
		testip = urllib2.urlopen('http://curlmyip.com').read()
		if checkValidIP(testip):
			return testip

		# 3rd try
		r = requests.get('http://ipaddr.me')
		testip = r.text
		if checkValidIP(testip):
			return testip

		# 4th try
		r = requests.get('http://www.icanhazip.com/')
		if checkValidIP(testip):
			return testip
		
	except urllib2.URLError:
		print('Error : Impossible d\'acceder aux sites IP!!')
		print('Verifier la connexion du reseau')
		return None

# Initialization
while(monip is None):
	print("test")
	monip = getPublicIP()
	# should add a timer here
	print monip

try:
	putdata = {'ip': monip, 'password': 'admin', 'rectype': 'A', 'reverse':0}
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	r = requests.put(url, data=json.dumps(putdata), headers=headers)
except requests.exceptions.ConnectionError:
	print("REST SERVER IS DOWN")
	#sys.exit("REST SERVER IS DOWN")

# Looping every 5 seconds
while(1):
	print('Start Loop')
	newip = getPublicIP()
	if newip != monip:
		monip = newip
		try:
			putdata = {'ip': newip, 'password': 'admin', 'rectype': 'A', 'reverse':0}
			headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
			r = requests.put(url, data=json.dumps(putdata), headers=headers)
		except requests.exceptions.ConnectionError:
			print("REST SERVER IS DOWN!!")
	time.sleep(5)

