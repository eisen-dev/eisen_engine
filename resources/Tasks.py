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
from threading import Thread

auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'ansible':
        return 'default'
    return None


task_fields = {
    'hosts': fields.String,
    'command': fields.String,
    'module': fields.String,
    'uri': fields.Url('task')
}

module = dispatcher.use_module()
tasks = dispatcher.TasksList(module)


class TasksAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('hosts', type=str, required=True,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('command', type=str, default="",
                                   location='json')
        self.reqparse.add_argument('module', type=str, default="",
                                   location='json')
        super(TasksAPI, self).__init__()

    def get(self):
        return {'tasks': [marshal(task, task_fields) for task in tasks]}

    def html_decode(self,s):
        """
        Returns the ASCII decoded version of the given HTML string. This does
        NOT remove normal HTML tags like <p>.
        """
        htmlCodes = (
                ("'", '&#39;'),
                ('"', '&quot;'),
                ('>', '&gt;'),
                ('<', '&lt;'),
                ('&', '&amp;')
            )
        for code in htmlCodes :
            s = s.replace(code[1], code[0])
        return s

    def post(self):
        args = self.reqparse.parse_args()
        task = {
            'id': tasks[-1]['id'] + 1,
            'hosts': args['hosts'],
            'command': self.html_decode(args['command']),
            'module': args['module'],
        }
        tasks.append(task)
        return {'task': marshal(task, task_fields)}, 201


class TaskAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('hosts', type=str, location='json')
        self.reqparse.add_argument('command', type=str, location='json')
        self.reqparse.add_argument('module', type=str, location='json')
        super(TaskAPI, self).__init__()

    def get(self, id):
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            abort(404)
        return {'task': marshal(task[0], task_fields)}

    def put(self, id):
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            abort(404)
        task = task[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                task[k] = v
        return {'task': marshal(task, task_fields)}

    def delete(self, id):
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            abort(404)
        tasks.remove(task[0])
        return {'result': True}


class TaskRunAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('hosts', type=str, location='json')
        self.reqparse.add_argument('command', type=str, location='json')
        self.reqparse.add_argument('module', type=str, location='json')
        super(TaskRunAPI, self).__init__()

    def get(self, id):
        task = [task for task in tasks if task['id'] == id]
        hosts = task[0]['hosts']
        command = task[0]['command']
        mod = task[0]['module']
        print mod
        print command
        print hosts
        task_fields = Thread(target=dispatcher.RunTask, args=[module, hosts, command, mod,
                                                           id])
        task_fields.start()
        task_json = {
            'started': str(task_fields.getName()),
        }
        if len(task) == 0:
            abort(404)
        return {'task': (task_json)}

    def put(self, id):
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            abort(404)
        task = task[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                task[k] = v
        return {'task': marshal(task, task_fields)}

    def delete(self, id):
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            abort(404)
        tasks.remove(task[0])
        return {'result': True}


class TaskResultAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('hosts', type=str, location='json')
        self.reqparse.add_argument('command', type=str, location='json')
        self.reqparse.add_argument('module', type=str, location='json')
        super(TaskResultAPI, self).__init__()

    def get(self, id):
        task = [task for task in tasks if task['id'] == id]
        hosts = task[0]['hosts']
        command = task[0]['command']
        mod = task[0]['module']
        print mod
        print command
        print hosts
        task_fields = dispatcher.ResultTask(id)
        if len(task) == 0:
            abort(404)
        return {'task': (task_fields)}

    def put(self, id):
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            abort(404)
        task = task[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                task[k] = v
        return {'task': marshal(task, task_fields)}

    def delete(self, id):
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            abort(404)
        tasks.remove(task[0])
        return {'result': True}
