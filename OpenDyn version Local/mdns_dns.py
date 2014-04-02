import socket
from zeroconf.dns import ServiceInfo
from zeroconf.mdns import Zeroconf
import localint
import sys
import httprequests


if __name__ == "__main__":
	z = Zeroconf("0.0.0.0")

	base_name = 'ns.local.'
	my_ip = localint.getLocalIP('www.google.fr')
	stype = '_dns._udp.local.'
	login = 'admin'
	password = 'admin'
	
	# registering DNS service and nameprobe on mDNS group
	try:
		full_name = '%s.%s'%( base_name.split('.')[0], stype )
		s = ServiceInfo(
			stype,
			full_name, # FQDN mDNS name of server
			server = base_name, # simplified servername (xx1.local.)
			address = socket.inet_aton(my_ip),
			port = 53,
			properties = {"hello":"world", "dept":"ricm"}, # Setting DNS TXT records...
		)
		z.registerService( s )
		serv_name = z.probeName( base_name )
		z.unregisterService( s )
		print 'Negotiated name:', serv_name
		s.server = serv_name	
		z.checkService( s )
		z.registerService( s )
	except:
		print("Error in name registration")

	#update DNS via REST
	url = 'https://'+login+':'+password+'@'+'127.0.0.1'+':5000/hosts'
	try:
		print('REST update.. ')
		post_name = serv_name.split('.')[0]
		putdata = {'ip': my_ip , 'hostname' : post_name , 'rectype' :'A'}
		httprequests.httpPost(url, putdata)
	except:
		print('Error on REST update.')
		z.close()

	finally :
		raw_input( 'Press <enter> to release name > ' )
		httprequests.httpDelete(url+'/'+post_name)
		z.close()


