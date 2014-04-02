'''
Module pour gerer les fichiers base de donnee DNS (bind9)
'''

# I/O modules
from tempfile import mkstemp
from shutil import move
from os import remove, close

#for managine PIDS
import psutil

#for sending signals
import psutil
import signal
import os

# generate a JSON dictionary of hosts from a zone file
def getDict(zonefile):
	zone_file = open(zonefile, 'r')
	my_dict = {}
	position = False
	for line in zone_file:
		if ';hostlist' in line:
			position = True
		if ';endhostlist' in line:
			break
		if(position==True):
			if(';hostlist' not in line):
				host = line.split('\t') #split the line by tabs
				hostname = host[0]
				hostrectype = host[2]
				hostipwithlinebreak = host[3]
				hostip = hostipwithlinebreak[:-1] # we remove the linebreak in the the last string
				my_dict[hostname] = {'ip' : hostip, 'rectype':hostrectype}
			if(';endhostlist' in line):
				pass
	zone_file.close()
	return my_dict
	

# replace a host IP address in a zonefile
def updateHostIP(hostname, zonefile, hostip, rectype):
	fh, abs_path = mkstemp() #Create temp file
	new_file = open(abs_path,'w')
	old_file = open(zonefile)
	subst = str(hostname+'\tIN\t'+ rectype+'\t'+ hostip)
	for line in old_file:
		if hostname in line:
			new_file.write(subst)
			new_file.write('\n')
		elif 'Serial' in line: #on incremente le serial a chaque modification
			for x in line.split():
				if x.isdigit():
					old_serial = x
					break
			new_serial = int(old_serial) + 1
			#format un peu decale mais bon
			new_file.write('\t' + '\t' + '\t' + str(new_serial) + '\t\t' + '; Serial' + '\n')
		else:
			new_file.write(line)
	new_file.close() #close temp file
	close(fh)
	old_file.close()
	remove(zonefile) #Remove original file
	move(abs_path, zonefile) #Move new file


# generate a default zonefile
def createZoneFile(zonename,domainip):
	new_file = open('db.'+zonename, 'w') #creer un nouveau fichier
	new_file.write(';\n;BIND zone data file for testopendyn.com\n;\n') #header
	new_file.write('$TTL	604800\n')
	new_file.write('@	IN	SOA	'+ 'ns.'+zonename+'.	'+ 'admin.'+zonename+'.	'+'(\n')
	new_file.write('			'+ '4		'+'; Serial\n')
	new_file.write('			'+ '604800		'+'; Refresh\n')
	new_file.write('			'+ '86400		'+'; Retry\n')
	new_file.write('			'+ '3600		'+'; Expire\n')
	new_file.write('			'+ '604800)		'+'; Negative Cache TTL\n\n')
	new_file.write(';adress of this domain \n')
	new_file.write('	IN	A	'+domainip+ '\n\n')
	new_file.write(';DNS Server\n')
	new_file.write('@	IN	NS	ns.'+zonename+'.\n\n')
	new_file.write(';hostlist\n')
	new_file.write('\n')
	new_file.write(';endhostlist\n')


# add a new host in a zonefile
def addNewHost(zonefile, hostname, hostip, rectype):
	fh, abs_path = mkstemp()
	new_file = open(abs_path,'w')
	old_file = open(zonefile)
	for line in old_file:
		if 'Serial' in line: #on incremente le serial a chaque modification
			for x in line.split():
				if x.isdigit():
					old_serial = x
					break
			new_serial = int(old_serial) + 1
			#format un peu decale mais bon
			new_file.write('\t' + '\t' + '\t' + str(new_serial) + '\t\t' + '; Serial' + '\n')
		else:
			new_file.write(line)
		if ';hostlist' in line:
			new_file.write(hostname + '\t' + 'IN	'+rectype+'\t' + hostip + '\n')
	new_file.close()
	close(fh)
	old_file.close()
	remove(zonefile)
	move(abs_path, zonefile)


# delete a host in a zonefile
def deleteHost(zonefile, hostname):
	fh, abs_path = mkstemp() #Create temp file
	new_file = open(abs_path,'w')
	old_file = open(zonefile)
	for line in old_file:
		if hostname in line:
			pass # on passe si on voit l'hote a supprimer
		elif 'Serial' in line: # on incremente le serial a chaque modification
			for x in line.split():
				if x.isdigit():
					old_serial = x
					break
			new_serial = int(old_serial) + 1
			#format un peu decale mais bon
			new_file.write('\t' + '\t' + '\t' + str(new_serial) + '\t\t' + '; Serial' + '\n')
		else:
			new_file.write(line)
	new_file.close() #close temp file
	close(fh)
	old_file.close()
	remove(zonefile) #Remove original file
	move(abs_path, zonefile) #Move new file


# updates a process(named) by sending SIGHUP(reloads configurations files :D)
def signalProc(proc_name):
	pids = psutil.get_pid_list() #lister tous les PID en cours
	for pid in pids:
		if proc_name in str(psutil.Process(pid).name):
			print ('Process <' + proc_name +'>')
			print ('PID : ' + str(pid))
			print (proc_name + ' is signaled with SIGHUP\n')	
			os.kill(pid,signal.SIGHUP)

