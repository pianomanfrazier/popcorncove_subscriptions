import os
import json
import tempfile
import base64

import pytest

from app import app, db

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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE']
    app.config['TESTING'] = True
    app.config['ADMIN_USER'] = 'TESTADMIN'
    app.config['ADMIN_PASSWORD'] = 'TESTPASSWORD'
    app.wsgi_app = FlaskTestClientProxy(app.wsgi_app)
    client = app.test_client()

    with app.app_context():
      db.create_all()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

def test_api(client):
  rv = client.get('/api/v1/')
  assert b'Popcorn Cove Subscriptions version 1' in rv.data

# Customer Tests

def test_create_customer(client):
  rv = client.post('/api/v1/customer', json=dict(
    name='Bob Jones',
    phone='(123) 456-7890',
    email='bob@jones.com'
  ))
  assert rv.status == '201 CREATED'

def test_customer(client):
  client.post('/api/v1/customer', json=dict(
    name='Bob Jones',
    phone='(123) 456-7890',
    email='bob@jones.com'
  ))
  rv = client.get('/api/v1/customer/1')
  assert b'Bob Jones' in rv.data

def test_update_customer(client):
  client.post('/api/v1/customer', json=dict(
    name='Bob Jones',
    phone='(123) 456-7890',
    email='bob@jones.com'
  ))
  client.put('/api/v1/customer/1', json=dict(
    name='Jimmy Jones',
    phone='(123) 456-7890',
    email='bob@jones.com'
  ))
  rv = client.get('/api/v1/customer/1')
  assert b'Jimmy Jones' in rv.data

def test_delete_customer(client):
  client.post('/api/v1/customer', json=dict(
    name='Bob Jones',
    phone='(123) 456-7890',
    email='bob@jones.com'
  ))
  rv = client.delete('/api/v1/customer/1')
  assert rv.status == '200 OK'

# ShippingAddress Tests
def test_create_address(client):
  client.post('/api/v1/customer', json=dict(
    name='Bob Jones',
    phone='(123) 456-7890',
    email='bob@jones.com'
  ))
  rv = client.post('/api/v1/shippingaddress', json=dict(
    customerID='1',
    address='123 N 1400 E',
    city='Leadville',
    state='Colorado',
    zip='12345'
  ))
  assert  rv.status == '201 CREATED'

def test_update_address(client):
  client.post('/api/v1/customer', json=dict(
    name='Bob Jones',
    phone='(123) 456-7890',
    email='bob@jones.com'
  ))
  client.post('/api/v1/shippingaddress', json=dict(
    customerID='1',
    address='123 N 1400 E',
    city='Leadville',
    state='Colorado',
    zip='12345'
  ))
  rv = client.put('/api/v1/shippingaddress/1', json=dict(
    customerID='1',
    address='543 N 1400 E',
    city='Leadville',
    state='Colorado',
    zip='12345'
  ))
  assert b'543' in rv.data

def test_get_addresses(client):
  client.post('/api/v1/customer', json=dict(
    name='Bob Jones',
    phone='(123) 456-7890',
    email='bob@jones.com'
  ))
  client.post('/api/v1/shippingaddress', json=dict(
    customerID='1',
    address='123 N 1400 E',
    city='Leadville',
    state='Colorado',
    zip='12345'
  ))
  rv = client.get('/api/v1/shippingaddress/1')
  assert  rv.status == '200 OK'

# Subscription Tests
def test_get_subscriptions(client):
  client.post('/api/v1/customer', json=dict(
    name='Bob Jones',
    phone='(123) 456-7890',
    email='bob@jones.com'
  ))
  client.post('/api/v1/shippingaddress', json=dict(
    customerID='1',
    address='123 N 1400 E',
    city='Leadville',
    state='Colorado',
    zip='12345'
  ))
  rv = client.post('/api/v1/subscription', json=dict(
    customerID        = '1',
    itemID            = '1',
    shippingAddressID = '1',
    startDate         = '2019-4',
    stopDate          = '2019-1',
    note              = 'Extra cheese please.' 
  ))
  assert rv.status == '201 CREATED'



# Item Tests
def test_create_items(client):
  client.post('/api/v1/item', json=dict(
    name='Popcorn'
  ))
  client.post('/api/v1/item', json=dict(
    name='Candy'
  ))
  rv = client.post('/api/v1/item', json=dict(
    name='Surprise'
  ))
  assert rv.status == '201 CREATED'
