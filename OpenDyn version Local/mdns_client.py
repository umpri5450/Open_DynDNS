import socket
from zeroconf.mdns import Zeroconf, ServiceBrowser
import sys
import time
import httprequests
import localint
from zeroconf.dns import ServiceInfo
from zeroconf.mdns import Zeroconf

# A listener class
class MyListener(object):
	def __init__(self,zc):
		self.r = zc
		self.address = ''

	def removeService(self, zeroconf, type_, name):
		print "Service", name, "removed"
	
	def addService(self, zeroconf, type_, name):
		print "Service", name, "added"
		print "Type is", type_
		info = None
		retries = 0
		while not info and retries < 10:
			info = self.r.getServiceInfo(type_, name)
			#info = r.getServiceInfo(type_, name)
			if not info:
				print "  (timeout)"
			retries += 1
		self.address = str(socket.inet_ntoa(info.getAddress()))
	
	def getServAddress(self):
		return self.address

# Main of the program
if __name__ == "__main__":
	#static variables
	print("Testing browsing for DNS service ")
	find_type = "_dns._udp.local."
	zc = Zeroconf('0.0.0.0')
	serv_ip = ''

	base_name = 'client.local.'
	client_ip = localint.getLocalIP('www.google.fr')
	client_type = '_http._tcp.local.'
	client_port = 55555
	login = 'admin'
	password = 'admin'
	

	#search for real DNS server by mDNS
	try:
		listener = MyListener(zc)
		browser = ServiceBrowser(zc , find_type, listener)
		serv_ip = listener.getServAddress()
		test = 0
		while(not serv_ip and test<5):
			time.sleep(1)
			serv_ip = listener.getServAddress()
			test += test
		print('Local IP of DNS server  : ' + serv_ip)
	except:
		print("Error in searching for DNS services")
		sys.exit(0)
	finally:
		print('DNS server found....')
        	zc.close()


	#register client service and nameprobe on mDNS
	try:
		zc = Zeroconf('0.0.0.0')
		full_name = '%s.%s'%( base_name.split('.')[0], client_type )
		print(full_name)
		s = ServiceInfo(
			client_type,
			full_name, # FQDN mDNS name of server
			server = base_name,
			address = socket.inet_aton(client_ip),
			port = client_port,
			properties = {"hello":"world", "dept":"ricm"}, # Setting DNS TXT records...
		)
		# we register/unregister twice to prevent name conflits by numbering client_name
		zc.registerService( s )
		client_name = zc.probeName( base_name )
		print(client_name)
		zc.unregisterService( s )
		print 'Negotiated name:', client_name
		s.server = client_name
		zc.checkService( s )
		zc.registerService( s )
	except:
		print("Error in name registration")
		zc.close()

    	finally:
		raw_input('Press <enter> to update DNS server via RESTs')

	#update DNS via REST
	url = 'https://'+login+':'+password+'@'+'127.0.0.1'+':5000/hosts'
	try:
		print('test')
		post_name = client_name.split('.')[0]
		putdata = {'ip': client_ip , 'hostname' : post_name , 'rectype' :'A'}
		httprequests.httpPost(url, putdata)
	except:
		print('Error on REST update.')
		zc.close()
	finally:
		raw_input('Press <enter> to exit application')
		httprequests.httpDelete(url+'/'+post_name)

	#exit program
	try:
		zc.close()
	except:
		print('Error exit')
	
