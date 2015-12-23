import base64
import json
from nose.tools import *

from tests import test_app


def check_content_type_json(headers):
    eq_(headers['Content-Type'], 'application/json')


def check_content_type_html(headers):
    eq_(headers['Content-Type'], 'text/html; charset=utf-8')


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
    get hosts

    :var
    Username: ansible
    Password: default
    """
    username = 'ansible'
    password = 'default'

    rv = test_app.get('/eisen/api/v1.0/hosts', headers={
        'Authorization': 'Basic ' + base64.b64encode(username +
                                                     ":" + password)
    })
    check_content_type_json(rv.headers)
    resp = json.loads(rv.data)
    # make sure we get a response
    eq_(rv.status_code, 200)
    # make sure there are no users
    eq_(len(resp), 1)


def test_post_new_host():
    """
    Post new host to /hosts

    :var
    Username: ansible
    Password: default
    Json data example
    """
    username = 'ansible'
    password = 'default'

    host = dict(host="192.168.233.132", groups="vmware")
    rv = test_app.post('/eisen/api/v1.0/hosts', data=json.dumps(host),
                       content_type='application/json',
                       headers={
                           'Authorization': 'Basic ' + base64.b64encode(username +
                                                                        ":" + password)
                       })
    check_content_type_json(rv.headers)
    # make sure we get a response
    eq_(rv.status_code, 201)


def test_host():
    """
    get host 1 information

    :var
    Username: ansible
    Password: default
    """
    username = 'ansible'
    password = 'default'

    rv = test_app.get('/eisen/api/v1.0/host/1',
                      headers={'Authorization': 'Basic ' +
                                                base64.b64encode(username +
                                                                 ":" + password)
                               })
    check_content_type_json(rv.headers)
    resp = json.loads(rv.data)
    # make sure we get a response
    eq_(rv.status_code, 200)
    # make sure there are no users
    eq_(len(resp), 1)
