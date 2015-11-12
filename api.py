#!flask/bin/python

"""Eisen API using Flask-RESTful extension."""

from flask import Flask, jsonify, abort, make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from flask.ext.httpauth import HTTPBasicAuth
from core import Ansible

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

hosts = Ansible.HostsList()

host_fields = {
    'hosts': fields.String,
    'jobs': fields.String,
    'group': fields.String,
    'busy': fields.Boolean,
    'uri': fields.Url('host')
}

class GroupsHostsAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('hosts', type=str, required=True,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('jobs', type=str, default="",
                                   location='json')
        self.reqparse.add_argument('group', type=str, default="",
                                   location='json')
        super(GroupsHostsAPI, self).__init__()

    def get(self):
        return {'hosts': [marshal(host, host_fields) for host in hosts]}

    def post(self):
        args = self.reqparse.parse_args()
        host = {
            'id': hosts[-1]['id'] + 1,
            'hosts': args['host'],
            'jobs': args['jobs'],
            'group': args['groups'],
            'busy': False
        }
        hosts.append(host)
        return {'host': marshal(host, host_fields)}, 201

class GroupsAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('host', type=str, location='json')
        self.reqparse.add_argument('jobs', type=str, location='json')
        self.reqparse.add_argument('groups', type=str, location='json')
        self.reqparse.add_argument('busy', type=bool, location='json')
        super(GroupsAPI, self).__init__()

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

class TasksHostsAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('hosts', type=str, required=True,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('jobs', type=str, default="",
                                   location='json')
        self.reqparse.add_argument('group', type=str, default="",
                                   location='json')
        super(TasksHostsAPI, self).__init__()

    def get(self):
        return {'hosts': [marshal(host, host_fields) for host in hosts]}

    def post(self):
        args = self.reqparse.parse_args()
        host = {
            'id': hosts[-1]['id'] + 1,
            'hosts': args['host'],
            'jobs': args['jobs'],
            'group': args['groups'],
            'busy': False
        }
        hosts.append(host)
        return {'host': marshal(host, host_fields)}, 201

class TasksAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('host', type=str, location='json')
        self.reqparse.add_argument('jobs', type=str, location='json')
        self.reqparse.add_argument('groups', type=str, location='json')
        self.reqparse.add_argument('busy', type=bool, location='json')
        super(TasksAPI, self).__init__()

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

api.add_resource(GroupsHostsAPI, '/todo/api/v1.0/hosts', endpoint='hosts')
api.add_resource(GroupsAPI, '/todo/api/v1.0/host/<int:id>', endpoint='host')
api.add_resource(TasksHostsAPI, '/todo/api/v1.0/tasks', endpoint='tasks')
api.add_resource(TasksAPI, '/todo/api/v1.0/task/<int:id>', endpoint='task')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')