from flask import Blueprint, jsonify, request
import hashlib
import json
from .authentication import requires_auth
from .models import Customer, Item, ShippingAddress, Subscription
from . import db

api = Blueprint('api', __name__)

@api.route('/', methods=['GET'])
def index():
    return jsonify({'msg': 'Popcorn Cove Subscriptions version 1'})

@api.context_processor
def create_model(model, data):
  item = model()
  item.from_dict(data)
  db.session.add(item)
  db.session.commit()
  return jsonify(item.to_dict()), 201

@api.context_processor
def update_model(model, id, data):
  item = model.query.get(id)
  item.from_dict(data)
  db.session.add(item)
  db.session.commit()
  return jsonify(item.to_dict()), 200

@api.context_processor
def delete_model(model, id):
    item = model.query.get(id)
    className = model.__name__
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'msg': className + ' deleted', 'error': False}), 200 
    else:
        return jsonify({'msg': className + ' not found', 'error': True}), 404


# Customer Routes
@api.route('/customer', methods=['GET'])
def get_customers():
  customers = Customer.query.all()
  return jsonify([i.to_dict() for i in customers]), 200

@api.route('/customer/<int:id>', methods=['GET'])
def get_customer(id):
  customer = Customer.query.get(id)
  return jsonify(customer.to_dict()), 200

@api.route('/customer', methods=['POST'])
def create_customer():
  data = request.get_json()
  return create_model(Customer, data)

@api.route('/customer/<int:id>', methods=['PUT'])
def update_customer(id):
  data = request.get_json()
  return update_model(Customer, id, data)

@api.route('/customer/<int:id>', methods=['DELETE'])
def delete_customer(id):
  return delete_model(Customer, id)

# Subscription Routes
@api.route('/subscription', methods=['GET'])
def get_subscriptions():
  subscriptions = Subscription.query.all()
  return jsonify([i.to_dict() for i in subscriptions]), 200

@api.route('/subscription/<int:id>', methods=['GET'])
def get_subscription(id):
  subscription = Subscription.query.get(id)
  return jsonify(subscription.to_dict()), 200

@api.route('/subscription', methods=['POST'])
def create_subscription():
  data = request.get_json()
  return create_model(Subscription, data)

@api.route('/subscription/<int:id>', methods=['PUT'])
def update_subscription(id):
  data = request.get_json()
  return update_model(Subscription, id, data)

@api.route('/subscription/<int:id>', methods=['DELETE'])
def delete_subscription(id):
  return delete_model(Subscription, id)

# ShippingAddress Routes
@api.route('/shippingaddress', methods=['GET'])
def get_shippingaddresss():
  shippingaddresss = ShippingAddress.query.all()
  return jsonify([i.to_dict() for i in shippingaddresss]), 200

@api.route('/shippingaddress/<int:id>', methods=['GET'])
def get_shippingaddress(id):
  shippingaddress = ShippingAddress.query.get(id)
  return jsonify(shippingaddress.to_dict()), 200

@api.route('/shippingaddress', methods=['POST'])
def create_shippingaddress():
  data = request.get_json()
  return create_model(ShippingAddress, data)

@api.route('/shippingaddress/<int:id>', methods=['PUT'])
def update_shippingaddress(id):
  data = request.get_json()
  return update_model(ShippingAddress, id, data)

@api.route('/shippingaddress/<int:id>', methods=['DELETE'])
def delete_shippingaddress(id):
  return delete_model(ShippingAddress, id)

# Item Routes
@api.route('/item', methods=['GET'])
def get_items():
  items = Item.query.all()
  return jsonify([i.to_dict() for i in items]), 200

@api.route('/item/<int:id>', methods=['GET'])
def get_item(id):
  item = Item.query.get(id)
  return jsonify(item.to_dict()), 200

@api.route('/item', methods=['POST'])
def create_item():
  data = request.get_json()
  return create_model(Item, data)

@api.route('/item/<int:id>', methods=['PUT'])
def update_item(id):
  data = request.get_json()
  return update_model(Item, id, data)

@api.route('/item/<int:id>', methods=['DELETE'])
def delete_item(id):
  return delete_model(Item, id)
