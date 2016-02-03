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
from core import package_work, dispatcher

auth = HTTPBasicAuth()

#TODO make password auth to be same for all resource
@auth.get_password
def get_password(username):
    if username == 'ansible':
        return 'default'
    return None

pack_fields = {
    'targetHost': fields.String,
    'targetOS': fields.String,
    'packageName': fields.String,
    'packageVersion': fields.String,
    'packageAction': fields.String,
    'uri': fields.Url('packages')
}

result_fields = {
    'Result': fields.String,
    'uri': fields.Url('packages')
}

packs = dispatcher.PackageUpdate()

class PackageActionAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('targetHost', type=str, required=True,
                           help='No task title provided',
                           location='json')
        self.reqparse.add_argument('targetOS', type=str, required=True,
                           help='No task title provided',
                           location='json')
        self.reqparse.add_argument('packageName', type=str, required=True,
                           help='No task title provided',
                           location='json')
        self.reqparse.add_argument('packageVersion', type=str,
                           help='No task title provided',
                           location='json')
        self.reqparse.add_argument('packageAction', type=str, required=True,
                           help='No task title provided',
                           location='json')
        super(PackageActionAPI, self).__init__()

    def get(self):
        #return make_response(jsonify({'message': 'These are not the package '
        #                                                       'you are looking
        # for'}), 403)
        return {'packs': [marshal(pack, pack_fields) for pack in packs]}

    def post(self):
        args = self.reqparse.parse_args()
        pack = {
            'id': packs[-1]['id'] + 1,
            'targetHost': args['targetHost'],
            'targetOS': args['targetOS'],
            'packageName': args['packageName'],
            'packageVersion': args['packageVersion'],
            'packageAction': args['packageAction'],
        }
        result = package_work.package_get(pack)
        result = {'Result':result}
        return {'agent': marshal(result, result_fields)}, 201