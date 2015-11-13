#!flask/bin/python

"""Eisen API using Flask-RESTful extension."""

from flask import Flask, jsonify, abort, make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from flask.ext.httpauth import HTTPBasicAuth
from core import dispatcher

app = Flask(__name__, static_url_path="")
api = Api(app)
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'ansible':
        return 'default'
    return None


@auth.error_handler
def unauthorized():
    # return 403 instead of 401 to prevent browsers from displaying the default
    # auth dialog
    return make_response(jsonify({'message': 'Unauthorized access'}), 403)

module = dispatcher.use_module()
groups = dispatcher.GroupsList(module)
hosts = dispatcher.HostsList(module)

host_fields = {
    'host': fields.String,
    'uri': fields.Url('host')
}

group_fields = {
    'hosts': fields.String,
    'group': fields.String,
    'uri': fields.Url('host')
}

class GroupsHostsAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('hosts', type=str, required=True,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('group', type=str, default="",
                                   location='json')
        super(GroupsHostsAPI, self).__init__()

    def get(self):
        return {'groups': [marshal(group, group_fields) for group in groups]}

    def post(self):
        args = self.reqparse.parse_args()
        group = {
            'id': hosts[-1]['id'] + 1,
            'host': args['host'],
            'group': args['groups'],
        }
        groups.append(group)
        return {'host': marshal(group, group_fields)}, 201

class GroupsAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('host', type=str, location='json')
        self.reqparse.add_argument('groups', type=str, location='json')
        super(GroupsAPI, self).__init__()

    def get(self, id):
        group = [group for group in groups if group['id'] == id]
        if len(group) == 0:
            abort(404)
        return {'host': marshal(group[0], group_fields)}

    def put(self, id):
        group = [group for group in groups if group['id'] == id]
        if len(group) == 0:
            abort(404)
        group = group[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                group[k] = v
        return {'host': marshal(group, group_fields)}

    def delete(self, id):
        group = [group for group in groups if group['id'] == id]
        if len(group) == 0:
            abort(404)
        groups.remove(group[0])
        return {'result': True}

class AllHostsAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('host', type=str, required=True,
                                   help='No task title provided',
                                   location='json')
        super(AllHostsAPI, self).__init__()

    def get(self):
        return {'host': [marshal(host, host_fields) for host in hosts]}

    def post(self):
        args = self.reqparse.parse_args()
        host = {
            'id': hosts[-1]['id'] + 1,
            'host': args['host'],
            'jobs': args['jobs'],
            'group': args['groups'],
            'busy': False
        }
        hosts.append(host)
        return {'host': marshal(host, host_fields)}, 201

class HostsAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('host', type=str, location='json')
        super(HostsAPI, self).__init__()

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

api.add_resource(GroupsHostsAPI, '/todo/api/v1.0/groups', endpoint='hosts')
api.add_resource(GroupsAPI, '/todo/api/v1.0/group/<int:id>', endpoint='host')
api.add_resource(AllHostsAPI, '/todo/api/v1.0/hosts', endpoint='tasks')
api.add_resource(HostsAPI, '/todo/api/v1.0/host/<int:id>', endpoint='task')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')