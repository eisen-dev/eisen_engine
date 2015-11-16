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

task_fields = {
    'hosts': fields.String,
    'group': fields.String,
    'uri': fields.Url('host')
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
        self.reqparse.add_argument('group', type=str, default="",
                                   location='json')
        super(TasksAPI, self).__init__()

    def get(self):
        return {'task': [marshal(task, task_fields) for task in tasks]}

    def post(self):
        args = self.reqparse.parse_args()
        task = {
            'id': tasks[-1]['id'] + 1,
            'host': args['host'],
            'group': args['groups'],
        }
        tasks.append(task)
        return {'task': marshal(task, task_fields)}, 201

class TaskAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('host', type=str, location='json')
        self.reqparse.add_argument('groups', type=str, location='json')
        super(TaskAPI, self).__init__()

    def get(self, id):
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            abort(404)
        return {'host': marshal(task[0], task_fields)}

    def put(self, id):
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            abort(404)
        task = task[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                task[k] = v
        return {'host': marshal(task, task_fields)}

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
        self.reqparse.add_argument('host', type=str, location='json')
        self.reqparse.add_argument('groups', type=str, location='json')
        super(TaskRunAPI, self).__init__()

    def get(self, id):
        task = [task for task in tasks if task['id'] == id]
        print (task)
        hosts='101010'
        command='eix'
        task_fields = dispatcher.RunTask(module, hosts, command)
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