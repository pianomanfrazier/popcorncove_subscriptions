from flask import Blueprint, jsonify, request, make_response
import hashlib
import io, pyexcel
from datetime import datetime
import json
from .authentication import requires_auth
from .models import Customer, Item, ShippingAddress, Subscription
from . import db

api = Blueprint('api', __name__)

@api.route('/', methods=['GET'])
@requires_auth
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
        return jsonify({'msg': className + ' not found', 'error': True}), 400


# Customer Routes
@api.route('/customer', methods=['GET'])
@requires_auth
def get_customers():
  customers = Customer.query.all()
  return jsonify([i.to_dict() for i in customers]), 200

@api.route('/customer/<int:id>', methods=['GET'])
@requires_auth
def get_customer(id):
  customer = Customer.query.get(id)
  return jsonify(customer.to_dict()), 200

@api.route('/customer', methods=['POST'])
@requires_auth
def create_customer():
  data = request.get_json()
  return create_model(Customer, data)

@api.route('/customer/<int:id>', methods=['PUT'])
@requires_auth
def update_customer(id):
  data = request.get_json()
  return update_model(Customer, id, data)

@api.route('/customer/<int:id>', methods=['DELETE'])
@requires_auth
def delete_customer(id):
  return delete_model(Customer, id)

# Subscription Routes
@api.route('/subscription', methods=['GET'])
@requires_auth
def get_subscriptions():
  subscriptions = Subscription.query.all()
  return jsonify([i.to_dict() for i in subscriptions]), 200

@api.route('/subscription/<int:id>', methods=['GET'])
@requires_auth
def get_subscription(id):
  subscriptions = Subscription.query.filter_by(customerID=id).all()
  return jsonify([i.to_dict() for i in subscriptions]), 200

@api.route('/subscription', methods=['POST'])
@requires_auth
def create_subscription():
  data = request.get_json()
  return create_model(Subscription, data)

@api.route('/subscription/<int:id>', methods=['PUT'])
@requires_auth
def update_subscription(id):
  data = request.get_json()
  return update_model(Subscription, id, data)

@api.route('/subscription/<int:id>', methods=['DELETE'])
@requires_auth
def delete_subscription(id):
  return delete_model(Subscription, id)

# ShippingAddress Routes
@api.route('/shippingaddress', methods=['GET'])
@requires_auth
def get_shippingaddresses():
  shippingaddresses = ShippingAddress.query.all()
  return jsonify([i.to_dict() for i in shippingaddresses]), 200

@api.route('/shippingaddress/<int:id>', methods=['GET'])
@requires_auth
def get_shippingaddress(id):
  """get all addresses by customer id"""
  shippingaddresses = ShippingAddress.query.filter_by(customerID=id).all()
  return jsonify([i.to_dict() for i in shippingaddresses]), 200

@api.route('/shippingaddress', methods=['POST'])
@requires_auth
def create_shippingaddress():
  data = request.get_json()
  return create_model(ShippingAddress, data)

@api.route('/shippingaddress/<int:id>', methods=['PUT'])
@requires_auth
def update_shippingaddress(id):
  data = request.get_json()
  return update_model(ShippingAddress, id, data)

@api.route('/shippingaddress/<int:id>', methods=['DELETE'])
@requires_auth
def delete_shippingaddress(id):
  return delete_model(ShippingAddress, id)

# Item Routes
@api.route('/item', methods=['GET'])
@requires_auth
def get_items():
  items = Item.query.all()
  return jsonify([i.to_dict() for i in items]), 200

@api.route('/item/<int:id>', methods=['GET'])
@requires_auth
def get_item(id):
  item = Item.query.get(id)
  return jsonify(item.to_dict()), 200

@api.route('/item', methods=['POST'])
@requires_auth
def create_item():
  data = request.get_json()
  return create_model(Item, data)

@api.route('/item/<int:id>', methods=['PUT'])
@requires_auth
def update_item(id):
  data = request.get_json()
  return update_model(Item, id, data)

@api.route('/item/<int:id>', methods=['DELETE'])
@requires_auth
def delete_item(id):
  # migrate all subscriptions with FK for that item
  migrationID = request.args.get('migrate')
  subscriptions = Subscription.query.filter_by(itemID=id).all()
  for i in subscriptions:
    i.itemID = migrationID
    db.session.add(i)
  db.session.commit()
  # then delete the item
  return delete_model(Item, id)

@api.route('/export', methods=['GET'])
@requires_auth
def export_subscriptions():
  year = request.args.get('year')
  month = request.args.get('month')
  date = datetime.strptime('{}-{}'.format(year, month), '%Y-%m')
  subscriptions = Subscription.query\
    .filter(date >= Subscription.startDate)\
    .filter(date <= Subscription.stopDate)\
    .join(Customer, Subscription.customerID == Customer.id)\
    .join(Item, Subscription.itemID == Item.id)\
    .join(ShippingAddress, Subscription.shippingAddressID == ShippingAddress.id)\
    .add_columns(
      Subscription.id,
      Subscription.note,
      Customer.name,
      Customer.email,
      Customer.phone,
      ShippingAddress.address,
      ShippingAddress.city,
      ShippingAddress.state,
      ShippingAddress.zip,
      Item.name.label("itemName"))\
    .all()

  header = ["SUBSCRIPTION ID", "NAME","STREET","CITY","STATE", "ZIP", "EMAIL", "PHONE", "ITEM", "NOTE"]
  data = [ header ]
  for i in subscriptions:
    sub = [i.id, i.name, i.address, i.city, i.state, i.zip, i.email, i.phone, i.itemName, i.note]
    data.append(sub)
  sheet = pyexcel.Sheet(data)
  dest = io.StringIO()
  sheet.save_to_memory("csv", dest)
  output = make_response(dest.getvalue())
  output.headers["Content-Disposition"] = "attachment; filename=export_{}-{}.csv".format(year, month)
  output.headers["Content-type"] = "text/csv"
  return output
