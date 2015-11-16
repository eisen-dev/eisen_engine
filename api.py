#!flask/bin/python

"""Eisen API using Flask-RESTful extension."""

from flask import Flask, jsonify, abort, make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from flask.ext.httpauth import HTTPBasicAuth
from resources import GroupsList
from resources import HostsList
from resources import Tasks

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

api.add_resource(GroupsList.GroupsAPI, '/todo/api/v1.0/groups', endpoint='groups')
api.add_resource(GroupsList.GroupAPI, '/todo/api/v1.0/group/<int:id>', endpoint='group')
api.add_resource(HostsList.HostsAPI, '/todo/api/v1.0/hosts', endpoint='hosts')
api.add_resource(HostsList.HostAPI, '/todo/api/v1.0/host/<int:id>', endpoint='host')
api.add_resource(Tasks.TasksAPI, '/todo/api/v1.0/tasks', endpoint='Tasks')
api.add_resource(Tasks.TaskAPI, '/todo/api/v1.0/task/<int:id>', endpoint='Task')
api.add_resource(Tasks.TaskRunAPI, '/todo/api/v1.0/task/<int:id>/run', endpoint='TaskRun')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')