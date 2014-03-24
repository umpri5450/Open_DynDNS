'''
Module pour gerer les modification dans un de fichier base de donnee DNS
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

#for chmod
import stat
  

# replace host IP address
def replaceHostIP(host_id, file_path, subst):
	#Create temp file
	fh, abs_path = mkstemp()
	new_file = open(abs_path,'w')
	old_file = open(file_path)
	for line in old_file:
		if host_id in line:
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
	#close temp file
	new_file.close()
	close(fh)
	old_file.close()
	#Remove original file
	remove(file_path)
	#Move new file
	move(abs_path, file_path)


# generer un fichier db de format par defaut sans hotes defini
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


# ajouter un nouveau host dans un fichier de base de donne DNS
def addNewHost(zonefile, hostname, hostip):
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
			new_file.write(hostname + '\t' + 'IN	A	' + hostip )
	new_file.close()
	close(fh)
	old_file.close()
	remove(zonefile)
	move(abs_path, zonefile)

# update bind9 process by sending SIGHUP(reloads configurations files :D)
def signalProc(proc_name):
	pids = psutil.get_pid_list() #lister tous les PID en cours
	for pid in pids:
		if proc_name in str(psutil.Process(pid).name):
			print ('Process <' + proc_name +'>')
			print ('PID : ' + str(pid))
			print (proc_name + ' is signaled with SIGHUP\n')	
			os.kill(pid,signal.SIGHUP)

