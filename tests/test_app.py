import os
import tempfile
import base64

import pytest

from app import app

@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    app.config['ADMIN_USER'] = 'TESTADMIN'
    app.config['ADMIN_PASSWORD'] = 'TESTPASSWORD'
    client = app.test_client()

    # with app.app_context():
    #     app.init_db()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def test_api(client):
  valid_credentials = base64.b64encode(b'TESTADMIN:TESTPASSWORD').decode('utf-8')
  rv = client.get('/api/v1/', headers={'Authorization': 'Basic ' + valid_credentials})
  assert b'Popcorn Cove Subscriptions version 1' in rv.data