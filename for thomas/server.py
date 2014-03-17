#for Flask REST-ful webserver
from flask import Flask
from flask.ext.restful import reqparse, abort, Api, Resource

#for replaceDNSconfig
from tempfile import mkstemp
from shutil import move
from os import remove, close

#for http basic authentification
from functools import wraps
from flask import request, Response

#for HTTPS test, creates SSL context with .key and .crt files generated with openssl and self-signed
from OpenSSL import SSL
context = SSL.Context(SSL.SSLv23_METHOD)
context.use_privatekey_file('server.key')
context.use_certificate_file('server.crt')

def check_auth(username, password):		#verification de login et mot de passe
    return username == 'admin' and password == 'admin'

def authenticate():
    return Response(
    'Vous n\'etes pas autorise a acceder a cette ressource\n'
    'Veuillez vous indentider avec votre login et mot de passe', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):		#il suffit ajouter @requires_auth devant ce qu'on veut proteger avec ce login et mot de passe
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


#Debut de Flask
app = Flask(__name__)
api = Api(app)

HOSTS = {
    'host1': {'ip': '11.11.11.11', 'password':'lolilol', 'rectype':'www', 'reverse':0}
}

password1 = 'admin'
domain = 'testopendyn.com'

def abort_if_host_doesnt_exist(host_id):
    if host_id not in HOSTS:
        abort(404, message="Host {} doesn't exist".format(host_id))

parser = reqparse.RequestParser()
parser.add_argument('ip', type=str, required=True, help='No IP address received')
parser.add_argument('password', type=str, required=True, help='No password received!!')
parser.add_argument('rectype', type=str)
parser.add_argument('reverse', type=int)

def modifyDict(host_id,ip,password,rectype,reverse):
	HOSTS[host_id] = {'ip': ip,'password':password,'rectype':rectype,'reverse':reverse}
	return HOSTS[host_id]

def replaceDNSconfig(host_id, file_path, pattern, subst):
	#Create temp file
	fh, abs_path = mkstemp()
	new_file = open(abs_path,'w')
	old_file = open(file_path)
	for line in old_file:
		if host_id in line:
			#new_file.write(line.replace(pattern,subst)) #problem with replace
			new_file.write(subst)
			new_file.write('\n')
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
			
# Host
#   show a single host item and lets you delete them
class Host(Resource):
    @requires_auth
    def get(self, host_id):
        abort_if_host_doesnt_exist(host_id)
        return HOSTS[host_id]

    @requires_auth
    def delete(self, host_id):
        abort_if_host_doesnt_exist(host_id)
        del HOSTS[host_id]
        return '', 204
    
    @requires_auth
    def put(self, host_id):
        args = parser.parse_args()
	if args['password'] == password1:
		host = HOSTS[host_id]
		old_ip = host['ip']
		new_ip = args['ip']
		rectype = args['rectype']
		reverse = args['reverse']	
		print(old_ip)
		print(new_ip)
		print(rectype)
		print(reverse)
		modified_host = modifyDict(host_id,new_ip,args['password'],rectype,reverse)
		replaceDNSconfig(host_id,'db.'+domain,host_id+'\tIN\t'+rectype+'\t'+old_ip,host_id+'\tIN\t'+rectype+'\t'+new_ip)
		return modified_host, 201
	print('password error, please retry')
	return '', 404
 

# HostList
#   shows a list of all hosts, and lets you POST to add new hosts
class HostList(Resource):
    @requires_auth
    def get(self):
        return HOSTS

    @requires_auth
    def post(self):
        args = parser.parse_args()
        host_id = 'host%d' % (len(HOSTS) + 1)
        HOSTS[host_id] = {'ip': args['task']}
        return HOSTS[host_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(HostList, '/hosts')
api.add_resource(Host, '/hosts/<string:host_id>')

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0',ssl_context=context)