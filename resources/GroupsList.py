from flask import Flask, jsonify, abort, make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from flask.ext.httpauth import HTTPBasicAuth
from core import dispatcher

auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'ansible':
        return 'default'
    return None
group_fields = {
    'hosts': fields.String,
    'group': fields.String,
    'uri': fields.Url('host')
}
module = dispatcher.use_module()
groups = dispatcher.GroupsList(module)

class GroupsAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('hosts', type=str, required=True,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('group', type=str, default="",
                                   location='json')
        super(GroupsAPI, self).__init__()

    def get(self):
        return {'groups': [marshal(group, group_fields) for group in groups]}

    def post(self):
        args = self.reqparse.parse_args()
        group = {
            'id': groups[-1]['id'] + 1,
            'host': args['host'],
            'group': args['groups'],
        }
        groups.append(group)
        return {'host': marshal(group, group_fields)}, 201

class GroupAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('host', type=str, location='json')
        self.reqparse.add_argument('groups', type=str, location='json')
        super(GroupAPI, self).__init__()

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