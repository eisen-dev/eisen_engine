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
        super(AgentAPI, self).__init__()

    def get(self):
        return {'agent': [marshal(host, agent_fields) for host in agents]}

    def post(self):
        args = self.reqparse.parse_args()
        host = {
            'id': agents[-1]['id'] + 1,
            'module': args['module'],
        }
        agents.append(host)
        return {'agent': marshal(host, agent_fields)}, 201