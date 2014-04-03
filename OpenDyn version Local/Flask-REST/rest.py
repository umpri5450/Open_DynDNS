#for Flask REST-ful webserver
from flask import Flask
from flask.ext.restful import reqparse, abort, Api, Resource

#for http basic authentification
from functools import wraps
from flask import request, Response

#for HTTPS test, creates SSL context with .key and .crt files
#generated with openssl and self-signed
from OpenSSL import SSL

#database editing module
import zonefilemgr
import time

#verification de login et mot de passe
#il suffit ajouter @requires_auth devant ce qu'on veut proteger avec ce login et mot de passe
def check_auth(username, password):
    return username == 'admin' and password == 'admin'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Vous n\'avez pas de droit a acceder ce site.\n'
    'Veuillez vous identifier', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


# Debut de Flask
app = Flask(__name__)
api = Api(app)

def abort_if_host_doesnt_exist(host_id):
    if host_id not in HOSTS:
        abort(404, message="Host {} doesn't exist".format(host_id))

def abort_if_host_already_exist(host_id):
    if host_id in HOSTS:
	abort(404, message="Host already exists in database".format(host_id))


# Parser to parse JSON arguments
# we put "required = True" only when the arguments are used in both PUT and POST
parser = reqparse.RequestParser()
parser.add_argument('ip', type=str, required=True, help='No IP address received')
parser.add_argument('rectype', type=str, required = True )
parser.add_argument('hostname', type=str, required=False)

def modifyDict(host_id,ip,rectype):
	HOSTS[host_id] = {'ip': ip , 'rectype':rectype}
	return HOSTS[host_id]

def addHostToDict(host_id,ip, rectype):
	HOSTS[host_id] = {'ip': ip, 'rectype' :rectype}
	return HOSTS[host_id]
			
# A single host item
# we can GET, DELETE, or PUT a single host item
class Host(Resource):
    @requires_auth
    def get(self, host_id):
        abort_if_host_doesnt_exist(host_id)
        return HOSTS[host_id]

    @requires_auth
    def delete(self, host_id):
        abort_if_host_doesnt_exist(host_id)
        del HOSTS[host_id]
	zonefilemgr.deleteHost(my_zone_file, host_id)
	zonefilemgr.signalProc('named')
        return '', 204
    
    @requires_auth
    def put(self, host_id):
	abort_if_host_doesnt_exist(host_id)
        args = parser.parse_args()
	host = HOSTS[host_id]
	old_ip = host['ip']
	new_ip = args['ip']
	rectype = args['rectype']
	modified_host = modifyDict(host_id,new_ip,rectype)
	zonefilemgr.updateHostIP(host_id, my_zone_file, new_ip, rectype)
	zonefilemgr.signalProc('named')
	return modified_host, 201
 

# Shows a list of all hosts
# we can GET the list of hosts or POST a new host
class HostList(Resource):
    @requires_auth
    def get(self):
        return HOSTS

    @requires_auth
    def post(self):
        args = parser.parse_args()
        host_id = args['hostname']
	abort_if_host_already_exist(host_id)
	ip = args['ip']
	rectype = args['rectype']
	new_host = addHostToDict(host_id, ip, rectype)
	zonefilemgr.addNewHost(my_zone_file,host_id,ip, rectype)
	zonefilemgr.signalProc('named')
        return new_host, 201

# Set-up FLASK REST-ful API routing here
api.add_resource(HostList, '/hosts')
api.add_resource(Host, '/hosts/<string:host_id>')

# main
if __name__ == '__main__':
    #variables
    domain = 'testopendyn.com'
    #put actual path of zonefile in the bind directory
    #my_zone_file = '/etc/bind/db.testopendyn.com'
    my_zone_file = 'db.testopendyn.com'
    HOSTS = zonefilemgr.getDict(my_zone_file)

    #creation de context SSL
    context = SSL.Context(SSL.SSLv23_METHOD)
    context.use_privatekey_file('server.key')
    context.use_certificate_file('server.crt')

    app.debug = True
    app.run(host = '0.0.0.0',ssl_context=context)
