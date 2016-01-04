#!flask/bin/python
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

"""Eisen API using Flask-RESTful extension."""

from flask import Flask, jsonify, abort, make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from flask.ext.httpauth import HTTPBasicAuth
from resources import GroupsList
from resources import HostsList
from resources import Tasks
from resources import AgentInfo
from bin import celery_work

app = Flask(__name__, static_url_path="")
celery_work.conf.update(app.config)


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

api.add_resource(AgentInfo.AgentAPI, '/eisen/api/v1.0/agent', endpoint='agent')

api.add_resource(GroupsList.GroupsAPI, '/eisen/api/v1.0/groups', endpoint='groups')
api.add_resource(GroupsList.GroupAPI, '/eisen/api/v1.0/group/<int:id>', endpoint='group')
api.add_resource(GroupsList.GroupVarsAPI, '/eisen/api/v1.0/group/<int:id>/vars',
                 endpoint='groupvars')
api.add_resource(HostsList.HostsAPI, '/eisen/api/v1.0/hosts', endpoint='hosts')
api.add_resource(HostsList.HostAPI, '/eisen/api/v1.0/host/<int:id>', endpoint='host')
api.add_resource(HostsList.HostVarsAPI, '/eisen/api/v1.0/host/<int:id>/vars',
                 endpoint='hostvars')
api.add_resource(Tasks.TasksAPI, '/eisen/api/v1.0/tasks', endpoint='tasks')
api.add_resource(Tasks.TaskAPI, '/eisen/api/v1.0/task/<int:id>', endpoint='task')
api.add_resource(Tasks.TaskRunAPI, '/eisen/api/v1.0/task/<int:id>/run',
                 endpoint='taskrun')
api.add_resource(Tasks.TaskResultAPI, '/eisen/api/v1.0/task/<int:id>/result',
                 endpoint='taskresult')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
