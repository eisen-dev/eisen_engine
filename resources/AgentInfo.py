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

auth = HTTPBasicAuth()

#TODO make password auth to be same for all resource
@auth.get_password
def get_password(username):
    if username == 'ansible':
        return 'default'
    return None

agent_fields = {
    'module': fields.String,
    'version': fields.String,
    'uri': fields.Url('host')
}

agents = dispatcher.AgentInfo()

class AgentAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('module', type=str, required=True,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('version', type=str, required=True,
                                   help='No task title provided',
                                   location='json')
        super(AgentAPI, self).__init__()

    def get(self):
        return {'agent': [marshal(host, agent_fields) for host in agents]}

    def post(self):
        args = self.reqparse.parse_args()
        host = {
            'id': agents[-1]['id'] + 1,
            'module': args['module'],
            'version': args['version'],
        }
        agents.append(host)
        return {'agent': marshal(host, agent_fields)}, 201