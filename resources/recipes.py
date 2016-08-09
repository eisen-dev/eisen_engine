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
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_httpauth import HTTPBasicAuth
from core import dispatcher
from threading import Thread

auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'ansible':
        return 'default'
    return None


recipe_fields = {
    'host': fields.String,
    'file': fields.String,
    'package': fields.String,
    'uri': fields.Url('task')
}

module = dispatcher.use_module()
recipes = dispatcher.RecipesList(module)


class recipesAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('host', type=str, required=True,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('file', type=str, default="",
                                   location='json')
        self.reqparse.add_argument('package', type=str, default="",
                                   location='json')
        super(recipesAPI, self).__init__()

    def get(self):
        return {'recipes': [marshal(recipe, recipe_fields) for recipe in recipes]}

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
            'id': recipes[-1]['id'] + 1,
            'host': args['host'],
            'file': self.html_decode(args['file']),
            'package': args['package'],
        }
        recipes.append(task)
        return {'task': marshal(task, recipe_fields)}, 201


class recipeAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('host', type=str, location='json')
        self.reqparse.add_argument('file', type=str, location='json')
        self.reqparse.add_argument('package', type=str, location='json')
        super(recipeAPI, self).__init__()

    def get(self, id):
        task = [task for task in recipes if task['id'] == id]
        if len(task) == 0:
            abort(404)
        return {'task': marshal(task[0], recipe_fields)}

    def put(self, id):
        task = [task for task in recipes if task['id'] == id]
        if len(task) == 0:
            abort(404)
        task = task[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                task[k] = v
        return {'task': marshal(task, recipe_fields)}

    def delete(self, id):
        task = [task for task in recipes if task['id'] == id]
        if len(task) == 0:
            abort(404)
        recipes.remove(task[0])
        return {'result': True}


class recipeRunAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('host', type=str, location='json')
        self.reqparse.add_argument('file', type=str, location='json')
        self.reqparse.add_argument('package', type=str, location='json')
        super(recipeRunAPI, self).__init__()

    def get(self, id):
        task = [task for task in recipes if task['id'] == id]
        hosts = task[0]['host']
        file = task[0]['file']
        package = task[0]['package']
        print (file)
        print (package)
        print (hosts)
        #task_fields = Thread(target=dispatcher.RunRecepie, args=[module, file, id])
        task_fields = dispatcher.RunRecipe(module, file, id)
        #task_fields.start()
        if len(task) == 0:
            abort(404)
        return {'task': (task_fields)}

    def put(self, id):
        task = [task for task in recipes if task['id'] == id]
        if len(task) == 0:
            abort(404)
        task = task[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                task[k] = v
        return {'task': marshal(task, recipe_fields)}

    def delete(self, id):
        task = [task for task in recipes if task['id'] == id]
        if len(task) == 0:
            abort(404)
        recipes.remove(task[0])
        return {'result': True}


class recipeResultAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('host', type=str, location='json')
        self.reqparse.add_argument('command', type=str, location='json')
        self.reqparse.add_argument('package', type=str, location='json')
        super(recipeResultAPI, self).__init__()

    def get(self, id):
        task = [task for task in recipes if task['id'] == id]
        hosts = task[0]['host']
        file = task[0]['file']
        package = task[0]['package']
        print file
        print package
        print hosts
        task_fields = dispatcher.ResultRecipe(id)
        if len(task) == 0:
            abort(404)
        return {'task': (task_fields)}

    def put(self, id):
        task = [task for task in recipes if task['id'] == id]
        if len(task) == 0:
            abort(404)
        task = task[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                task[k] = v
        return {'task': marshal(task, recipe_fields)}

    def delete(self, id):
        task = [task for task in recipes if task['id'] == id]
        if len(task) == 0:
            abort(404)
        recipes.remove(task[0])
        return {'result': True}
