from flask import Blueprint, jsonify, request
import hashlib
import json
from .authentication import requires_auth
from .models import Customer
from . import db

api = Blueprint('api', __name__)

@api.route('/', methods=['GET'])
def index():
    return jsonify({'msg': 'Popcorn Cove Subscriptions version 1'})

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
  customer = Customer()
  customer.from_dict(data)
  db.session.add(customer)
  db.session.commit()
  return jsonify(customer.to_dict()), 201

@api.route('/customer/<int:id>', methods=['PUT'])
def update_customer(id):
  data = request.get_json()
  customer = Customer.query.get(id)
  customer.from_dict(data)
  db.session.add(customer)
  db.session.commit()
  return jsonify(customer.to_dict()), 200

@api.route('/customer/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get(id)
    if customer:
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'msg':'Comment deleted', 'error': False}), 200 
    else:
        return jsonify({'msg':'Comment not found', 'error': True}), 404