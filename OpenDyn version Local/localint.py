import socket

# Get the local ip of the default active interface
def getLocalIP(testTarget):
	address = ''
	try:
		s= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		s.connect((testTarget,65432))
		address = s.getsockname()[0]
		s.close()
		#checkValidIP(address)
	except:
		print("ERROR : Get local ip failed.")
	finally:
		#if checkValidIP(address):
		return address



# Check the format of an IP address
def checkValidIP(addr):
	try:
		print('Checking IP format.....')
		socket.inet_aton(addr)
		return True

	except socket.error:
		print("WRONG IP FORMAT")
		return False
