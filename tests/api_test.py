import base64
import json
import sys
from nose.tools import *
import time

# logging with nose
import logging

stream_handler = logging.StreamHandler(sys.__stderr__)
stream_handler.setFormatter(logging.Formatter('%(levelname)s :: '
                                              '%(name)s :: %(message)s'))
log = logging.getLogger()
log.addHandler(stream_handler)
log.setLevel(logging.DEBUG)
log2 = logging.getLogger(__name__)
log2.setLevel(logging.DEBUG)

from tests import test_app


def check_content_type_json(headers):
    eq_(headers['Content-Type'], 'application/json')


def check_content_type_html(headers):
    eq_(headers['Content-Type'], 'text/html; charset=utf-8')


# only function name starting with test are execute by nose
def test_failed_auth():
    """
    failing Basic Auth

    sending no header
    """
    rv = test_app.get('/eisen/api/v1.0/agent')
    check_content_type_html(rv.headers)
    eq_(rv.data, 'Unauthorized Access')
    # make sure we get a response
    eq_(rv.status_code, 401)


def test_success_auth():
    """
    Succesful Basic Auth
    Request agent

    :var
    Username: ansible
    Password: default
    """
    username = 'ansible'
    password = 'default'

    rv = test_app.get('/eisen/api/v1.0/agent', headers={
        'Authorization': 'Basic ' + base64.b64encode(username +
                                                     ":" + password)
    })
    check_content_type_json(rv.headers)
    resp = json.loads(rv.data)
    # make sure we get a response
    eq_(rv.status_code, 200)
    # make sure there are no users
    eq_(len(resp), 1)


def test_hosts():
    """
    get hosts information

    :var
    Username: ansible
    Password: default
    """
    log = logging.getLogger('hosts')
    username = 'ansible'
    password = 'default'

    rv = test_app.get('/eisen/api/v1.0/hosts', headers={
        'Authorization': 'Basic ' + base64.b64encode(username +
                                                     ":" + password)
    })
    check_content_type_json(rv.headers)
    resp = json.loads(rv.data)
    log.debug(rv.data)
    # make sure we get a response
    eq_(rv.status_code, 200)
    # make sure there are no users
    eq_(len(resp), 1)


def test_post_new_host():
    """
    Testing Post
    Adding new host to /hosts

    :var
    Username: ansible
    Password: default
    Json data example
    """
    log = logging.getLogger('post_new_host')
    username = 'ansible'
    password = 'default'

    host = dict(host="127.0.0.1", groups="vmware")
    rv = test_app.post('/eisen/api/v1.0/hosts', data=json.dumps(host),
                       content_type='application/json',
                       headers={
                           'Authorization': 'Basic ' + base64.b64encode(username +
                                                                        ":" + password)
                       })
    check_content_type_json(rv.headers)
    log.debug(rv.headers)
    # make sure we get a response
    eq_(rv.status_code, 201)

def test_recheck_hosts():
    """
    get hosts information

    :var
    Username: ansible
    Password: default
    """
    log = logging.getLogger('hosts')
    username = 'ansible'
    password = 'default'

    rv = test_app.get('/eisen/api/v1.0/hosts', headers={
        'Authorization': 'Basic ' + base64.b64encode(username +
                                                     ":" + password)
    })
    check_content_type_json(rv.headers)
    resp = json.loads(rv.data)
    log.debug(rv.data)
    # make sure we get a response
    eq_(rv.status_code, 200)
    # make sure there are no users
    eq_(len(resp), 1)

def test_host_vars():
    """
    get host 1 vars

    :var
    Username: ansible
    Password: default
    """
    log = logging.getLogger('test_host_vars')
    username = 'ansible'
    password = 'default'

    rv = test_app.get('/eisen/api/v1.0/host/1/vars',
                      headers={'Authorization': 'Basic ' +
                                                base64.b64encode(username +
                                                                 ":" + password)
                               })
    check_content_type_json(rv.headers)
    resp = json.loads(rv.data)
    log.debug(rv.data)
    # make sure we get a response
    eq_(rv.status_code, 200)
    # make sure there are no users
    eq_(len(resp), 1)

def test_add_vars_1():
    """
    Testing Post
    Adding new host to /hosts

    :var
    Username: ansible
    Password: default
    Json data example
    """
    log = logging.getLogger('post_new_host')
    username = 'ansible'
    password = 'default'

    var = dict(variable_key="ansible_ssh_port", variable_value="2222", host="localhost")
    rv = test_app.post('/eisen/api/v1.0/host/2/vars', data=json.dumps(var),
                       content_type='application/json',
                       headers={
                           'Authorization': 'Basic ' + base64.b64encode(username +
                                                                        ":" + password)
                       })
    check_content_type_json(rv.headers)
    log.debug(rv.headers)
    # make sure we get a response
    eq_(rv.status_code, 201)

def test_add_vars_2():
    """
    Testing Post
    Adding new host to /hosts

    :var
    Username: ansible
    Password: default
    Json data example
    """
    log = logging.getLogger('post_new_host')
    username = 'ansible'
    password = 'default'

    var = dict(variable_key="ansible_port", variable_value="2222", host="127.0.0.1")
    rv = test_app.post('/eisen/api/v1.0/host/2/vars', data=json.dumps(var),
                       content_type='application/json',
                       headers={
                           'Authorization': 'Basic ' + base64.b64encode(username +
                                                                        ":" + password)
                       })
    check_content_type_json(rv.headers)
    log.debug(rv.headers)
    # make sure we get a response
    eq_(rv.status_code, 201)

def test_recheck_host_vars():
    """
    get host 1 vars

    :var
    Username: ansible
    Password: default
    """
    log = logging.getLogger('test_host_vars')
    username = 'ansible'
    password = 'default'

    rv = test_app.get('/eisen/api/v1.0/host/1/vars',
                      headers={'Authorization': 'Basic ' +
                                                base64.b64encode(username +
                                                                 ":" + password)
                               })
    check_content_type_json(rv.headers)
    resp = json.loads(rv.data)
    log.debug(rv.data)
    # make sure we get a response
    eq_(rv.status_code, 200)
    # make sure there are no users
    eq_(len(resp), 1)
    # check to have added var to host
    #eq_(resp["var"][0]["variable_key"], "ansible_ssh_port")

def test_host():
    """
    get host 1 information

    :var
    Username: ansible
    Password: default
    """
    log = logging.getLogger('host')
    username = 'ansible'
    password = 'default'

    rv = test_app.get('/eisen/api/v1.0/host/1',
                      headers={'Authorization': 'Basic ' +
                                                base64.b64encode(username +
                                                                 ":" + password)
                               })
    check_content_type_json(rv.headers)
    resp = json.loads(rv.data)
    log.debug(rv.data)
    # make sure we get a response
    eq_(rv.status_code, 200)
    # make sure there are no users
    eq_(len(resp), 1)


def test_tasks():
    """
    Get all tasks informations

    :var
    Username: ansible
    Password: default
    """
    log = logging.getLogger('tasks')
    username = 'ansible'
    password = 'default'

    rv = test_app.get('/eisen/api/v1.0/tasks',
                      headers={'Authorization': 'Basic ' +
                                                base64.b64encode(username +
                                                                 ":" + password)
                               })
    check_content_type_json(rv.headers)
    resp = json.loads(rv.data)
    log.debug(rv.data)
    # make sure we get a response
    eq_(rv.status_code, 200)
    # make sure there are no users
    eq_(len(resp), 1)


def test_task():
    """
    Test execution of default task 1
    ping to localhost

    :var
    Username: ansible
    Password: default
    """
    log = logging.getLogger('task')
    username = 'ansible'
    password = 'default'

    rv = test_app.get('/eisen/api/v1.0/task/1/run',
                      headers={'Authorization': 'Basic ' +
                                                base64.b64encode(username +
                                                                 ":" + password)
                               })
    check_content_type_json(rv.headers)
    resp = json.loads(rv.data)
    log.debug(rv.data)
    # make sure we get a response
    eq_(rv.status_code, 200)
    # make sure there are no users
    eq_(len(resp), 1)
    #eq_(resp["task"]['contacted']['localhost']["ping"], "pong")

def test_task_result():
    """
    Test execution of default task 1
    ping to localhost

    :var
    Username: ansible
    Password: default
    """
    log = logging.getLogger('task')
    username = 'ansible'
    password = 'default'

    rv = test_app.get('/eisen/api/v1.0/task/1/result',
                      headers={'Authorization': 'Basic ' +
                                                base64.b64encode(username +
                                                                 ":" + password)
                               })
    check_content_type_json(rv.headers)
    resp = json.loads(rv.data)
    log.debug(rv.data)
    # make sure we get a response
    eq_(rv.status_code, 200)
    # make sure there are no users
    eq_(len(resp), 1)
    #eq_(resp["task"]['contacted']['localhost']["ping"], "pong")

    # check if now the task is ready
    time.sleep(2)
    rv = test_app.get('/eisen/api/v1.0/task/1/result',
                      headers={'Authorization': 'Basic ' +
                                                base64.b64encode(username +
                                                                 ":" + password)
                               })
    check_content_type_json(rv.headers)
    resp = json.loads(rv.data)
    log.debug(rv.data)
    # make sure we get a response
    eq_(rv.status_code, 200)
    # make sure there are no users
    eq_(len(resp), 1)
    #eq_(resp["task"]['contacted']['localhost']["ping"], "pong")


def test_add_new_task():
    """
    Testing Post
    Adding new host to /hosts

    :var
    Username: ansible
    Password: default
    Json data example
    """
    log = logging.getLogger('post_new_host')
    username = 'ansible'
    password = 'default'

    host = dict(hosts="localhost", module="ping")
    rv = test_app.post('/eisen/api/v1.0/tasks', data=json.dumps(host),
                       content_type='application/json',
                       headers={
                           'Authorization': 'Basic ' + base64.b64encode(username +
                                                                        ":" + password)
                       })
    check_content_type_json(rv.headers)
    log.debug(rv.headers)
    # make sure we get a response
    eq_(rv.status_code, 201)


def test_added_task():
    """
    Test execution of default task 1
    ping

    :var
    Username: ansible
    Password: default
    """
    log = logging.getLogger('task')
    username = 'ansible'
    password = 'default'

    rv = test_app.get('/eisen/api/v1.0/task/2/run',
                      headers={'Authorization': 'Basic ' +
                                                base64.b64encode(username +
                                                                 ":" + password)
                               })
    check_content_type_json(rv.headers)
    resp = json.loads(rv.data)
    log.debug(rv.data)
    # make sure we get a response
    eq_(rv.status_code, 200)
    # make sure there are no users
    eq_(len(resp), 1)
    #eq_(resp["task"]['contacted']['localhost']["ping"], "pong")


def test_added_task_result():
    """
    Test execution of default task 1
    ping

    :var
    Username: ansible
    Password: default
    """
    log = logging.getLogger('task')
    username = 'ansible'
    password = 'default'

    rv = test_app.get('/eisen/api/v1.0/task/2/result',
                      headers={'Authorization': 'Basic ' +
                                                base64.b64encode(username +
                                                                 ":" + password)
                               })
    check_content_type_json(rv.headers)
    resp = json.loads(rv.data)
    log.debug(rv.data)
    # make sure we get a response
    eq_(rv.status_code, 200)
    # make sure there are no users
    eq_(len(resp), 1)
    #eq_(resp["task"]['contacted']['localhost']["ping"], "pong")

    time.sleep(2)
    rv = test_app.get('/eisen/api/v1.0/task/2/result',
                      headers={'Authorization': 'Basic ' +
                                                base64.b64encode(username +
                                                                 ":" + password)
                               })
    check_content_type_json(rv.headers)
    resp = json.loads(rv.data)
    log.debug(rv.data)
    # make sure we get a response
    eq_(rv.status_code, 200)
    # make sure there are no users
    eq_(len(resp), 1)
    #eq_(resp["task"]['contacted']['localhost']["ping"], "pong")

def test_added_hosts():
    """
    Check if added host is present.

    :var
    Username: ansible
    Password: default
    """
    log = logging.getLogger('added_hosts')
    username = 'ansible'
    password = 'default'

    rv = test_app.get('/eisen/api/v1.0/host/2', headers={
        'Authorization': 'Basic ' + base64.b64encode(username +
                                                     ":" + password)
    })
    check_content_type_json(rv.headers)
    resp = json.loads(rv.data)
    log.debug(rv.data)
    # make sure we get a response
    eq_(rv.status_code, 200)
    # make sure there are no users
    eq_(len(resp), 1)
    eq_(resp["host"]["host"], "127.0.0.1")
    eq_(resp["host"]["groups"], "vmware")


def test_added_host_vars():
    """
    Check for variable associated to added host

    :var
    Username: ansible
    Password: default
    """
    log = logging.getLogger('added_host_vars')
    username = 'ansible'
    password = 'default'

    rv = test_app.get('/eisen/api/v1.0/host/2/vars',
                      headers={'Authorization': 'Basic ' +
                                                base64.b64encode(username +
                                                                 ":" + password)
                               })
    check_content_type_json(rv.headers)
    resp = json.loads(rv.data)
    # log.debug(rv.data)
    log2.debug(rv.data)
    # make sure we get a response
    #eq_(rv.status_code, 200)
    # make sure there are no users
    #eq_(len(resp), 1)