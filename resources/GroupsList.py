# (c) 2015, Alice Ferrazzi <alice.ferrazzi@gmail.com>
#
# This file is part of Eisen
#
# Eisen is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Eisen is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Eisen.  If not, see <http://www.gnu.org/licenses/>.

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
    'uri': fields.Url('group')
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
            'hosts': args['hosts'],
            'group': args['groups'],
        }
        groups.append(group)
        return {'host': marshal(group, group_fields)}, 201


class GroupAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('hosts', type=str, location='json')
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

class GroupVarsAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('group', type=str, location='json')
        self.reqparse.add_argument('variable', type=str, location='json')
        self.reqparse.add_argument('group', type=str, location='json')
        super(GroupVarsAPI, self).__init__()

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