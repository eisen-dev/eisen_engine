from flask import Flask, jsonify, abort, make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from flask.ext.httpauth import HTTPBasicAuth
from core import dispatcher

auth = HTTPBasicAuth()

#TODO make password auth to be same for all resource
@auth.get_password
def get_password(username):
    if username == 'ansible':
        return 'default'
    return None

host_fields = {
    'host': fields.String,
    'groups': fields.String,
    'uri': fields.Url('host')
}
module = dispatcher.use_module()
hosts = dispatcher.HostsList(module)

class HostsAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('host', type=str, required=True,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('groups', type=str, required=True,
                                   help='No task title provided',
                                   location='json')
        super(HostsAPI, self).__init__()

    def get(self):
        return {'host': [marshal(host, host_fields) for host in hosts]}

    def post(self):
        args = self.reqparse.parse_args()
        host = {
            'id': hosts[-1]['id'] + 1,
            'host': args['host'],
            'groups': args['host'],
        }
        hosts.append(host)
        return {'host': marshal(host, host_fields)}, 201

class HostAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('host', type=str, location='json')
        super(HostAPI, self).__init__()

    def get(self, id):
        host = [host for host in hosts if host['id'] == id]
        if len(host) == 0:
            abort(404)
        return {'host': marshal(host[0], host_fields)}

    def put(self, id):
        host = [host for host in hosts if host['id'] == id]
        if len(host) == 0:
            abort(404)
        host = host[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                host[k] = v
        return {'host': marshal(host, host_fields)}

    def delete(self, id):
        host = [host for host in hosts if host['id'] == id]
        if len(host) == 0:
            abort(404)
        hosts.remove(host[0])
        return {'result': True}