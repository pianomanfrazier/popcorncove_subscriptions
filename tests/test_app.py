import os
import tempfile
import base64

import pytest

from app import app

class FlaskTestClientProxy(object):
  """
  see https://stackoverflow.com/questions/15278285/setting-mocking-request-headers-for-flask-app-unit-test
  """
  def __init__(self, app):
    self.app = app

  def __call__(self, environ, start_response):
    valid_credentials = base64.b64encode(b'TESTADMIN:TESTPASSWORD').decode('utf-8')
    environ['Authorization'] = 'Basic ' + valid_credentials
    return self.app(environ, start_response)


@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    app.config['ADMIN_USER'] = 'TESTADMIN'
    app.config['ADMIN_PASSWORD'] = 'TESTPASSWORD'
    app.wsgi_app = FlaskTestClientProxy(app.wsgi_app)
    client = app.test_client()

    # with app.app_context():
    #     app.init_db()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def test_api(client):
  rv = client.get('/api/v1/')
  assert b'Popcorn Cove Subscriptions version 1' in rv.data