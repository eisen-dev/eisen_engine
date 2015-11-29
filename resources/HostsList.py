# (c) 2012-2015, Alice Ferrazzi <alice.ferrazzi@gmail.com>
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
import core.AnsibleInv as ans_inv
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
        self.reqparse.add_argument('groups', type=str, default="",
                                   location='json')
        super(HostsAPI, self).__init__()

    def get(self):
        return {'host': [marshal(host, host_fields) for host in hosts]}

    def post(self):
        args = self.reqparse.parse_args()
        inv_host = ans_inv.set_host(args['host'],'22')
        inv_host = ans_inv.set_host_variable('ansible_ssh_pass','3mendo3',inv_host)
        inv_group = ans_inv.set_group(args['groups'])
        inv_group = ans_inv.set_group_host(inv_group,inv_host)
        ans_inv.set_inv(inv_group)
        host = {
            'id': hosts[-1]['id'] + 1,
            'host': args['host'],
            'groups': args['groups'],
        }
        hosts.append(host)
        inv = ans_inv.get_inv()
        print (inv.groups_list())
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