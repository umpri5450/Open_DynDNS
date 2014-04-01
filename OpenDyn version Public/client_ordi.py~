import requests
import urllib2
import socket
import json
import time
import sys
import httprequests

'''
Daemon client pour les machines Open DynDNS version public
'''

#fonction pour checker le format d'une adresse IP
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
def getPublicIP(siteip):
	try:# 1st try with urllib2
		testip = urllib2.urlopen(siteip).read()
		if checkValidIP(testip):
			return testip
	except:
		print('Error : Impossible d\'acceder au site IP!!')
		testip = None

	try:# 2nd try with requests
		r = requests.get(siteip)
		testip = r.text
		if checkValidIP(testip):
			return testip
	except:
		print('Error : Impossible d\'acceder au site IP!!')
		testip = None

	return testip



# Main of the daemon
if __name__ == '__main__':
	# static variables
	url = 'https://admin:admin@127.0.0.1:5000/hosts/host1'
	monip = None
	'''
	Recuperation adresse IP publique 
	http://ip.42.pl/raw
	http://curlmyip.com
	http://ipaddr.me
	http://www.icanhazip.com/
	'''
	my_ip_server = 'http://ip.42.pl/raw'
	

	while(monip is None):
		print("test")
		monip = getPublicIP(my_ip_server)
		time.sleep(2)
		print monip

	'''
	La mise a jour de la premiere fois dans un reseau etranger
	Il faut mettre a jour le serveur au moins une fois avant de passer dans la boucle pour minimiser les requetes HTTP
	'''
	first_update = False
	while(first_update == False):
		try:
			putdata = {'ip': monip, 'rectype' : 'A'}
			s_code = httprequests.httpPut(url,putdata)
			print("First REST update....")
			print('Put reply status code :' +str(s_code) )
			first_update=True
		except requests.exceptions.ConnectionError:
			print("REST SERVER IS DOWN!!")
			time.sleep(10) # si le serveur n'est pas disponible, on attend avant de reboucler

	'''
	Looping every x seconds
	'''
	print('Start loop')
	while(1):
		try:
			print('Looping')
			newip = getPublicIP(my_ip_server)
			if newip != monip:
				monip = newip
				try:
					putdata = {'ip': newip,'rectype' : 'A'}
					s_code = httprequests.httpPut(url,putdata)
					print("REST server updated ")
					print('Put reply status code :' +str(s_code) )
				except requests.exceptions.ConnectionError:
					print("REST SERVER IS DOWN!!")
			time.sleep(5)
		except KeyboardInterrupt:
			print("\nGOODBYE!! \n")
			sys.exit(0)
