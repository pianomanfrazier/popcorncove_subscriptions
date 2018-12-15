from flask import abort
import hashlib
from . import db
from . import app
from sqlalchemy.sql import func

class Customer(db.Model):
  __tablename__ = 'customer'
  id            = db.Column(db.Integer, primary_key=True)
  name          = db.Column(db.String(70), unique=True, index=True)
  phone         = db.Column(db.String(25), unique=True, index=True)
  email         = db.Column(db.String(255), unique=True, index=True)
  time_created  = db.Column(db.DateTime(timezone=True), server_default=func.now(), index=True) 

  def __repr__(self):
    return '<Customer {}>'.format(self.name)

  def to_dict(self):
    return {
      'id': self.id,
      'name': self.name,
      'phone': self.phone,
      'email': self.email,
      'time_created': self.time_created
    }
  
  def from_dict(self, data):
    try:
      self.name = data['name']
      self.phone = data['phone']
      self.email = data['email']
    except KeyError:
      abort(400)

class Subscription(db.Model):
  __tablename__     = 'subscription'
  id                = db.Column(db.Integer, primary_key=True)
  customerID        = db.Column(db.Integer, db.ForeignKey('customer.id')) 
  itemID            = db.Column(db.Integer, db.ForeignKey('item.id')) 
  shippingAddressID = db.Column(db.Integer, db.ForeignKey('shippingaddress.id'))
  startDate         = db.Column(db.Date)
  stopDate          = db.Column(db.Date)
  note              = db.Column(db.String(255))

  def __repr__(self):
    return '<Subscription {}>'.format(self.id)

  def to_dict(self):
    return {
      'id'                : self.id,
      'customerID'        : self.customerID, 
      'itemID'            : self.itemId,
      'shippingAddressID' : self.shippingAddressID,
      'startDate'         : self.startDate,
      'stopDate'          : self.stopDate,
      'note'              : self.note
    }
  
  def from_dict(self, data):
    try:
      self.customerID        = data['customerID'] 
      self.itemID            = data['itemID'] 
      self.shippingAddressID = data['shippingAddressID'] 
      self.startDate         = data['startDate'] 
      self.stopDate          = data['stopDate'] 
      self.note              = data['note'] 
    except KeyError:
      abort(400)


class Item(db.Model):
  __tablename = 'item'
  id          = db.Column(db.Integer, primary_key=True)
  name        = db.Column(db.String(25))

  def __repr__(self):
    return '<Item {}>'.format(self.name)

  def to_dict(self):
    return {
      'id': self.id,
      'name': self.name,
    }
  
  def from_dict(self, data):
    try:
      self.name = data['name']
    except KeyError:
      abort(400)

class ShippingAddress(db.Model):
  __tablename__ = 'shippingaddress'
  id            = db.Column(db.Integer, primary_key=True)
  customerID    = db.Column(db.Integer, db.ForeignKey('customer.id')) 
  address       = db.Column(db.String(100))
  city          = db.Column(db.String(40))
  state         = db.Column(db.String(40))
  zip           = db.Column(db.String(11))

  def __repr__(self):
    return '<ShippingAddress {}>'.format(self.address)

  def to_dict(self):
    return {
      'customerID'   : self.customerID, 
      'address'      : self.address, 
      'city'         : self.city, 
      'state'        : self.state, 
      'zip'          : self.zip
    }
  
  def from_dict(self, data):
    try:
      self.id            = data['id'] 
      self.customerID    = data['customerID'] 
      self.address       = data['address'] 
      self.city          = data['city'] 
      self.state         = data['state'] 
      self.zip           = data['zip'] 
    except KeyError:
      abort(400)
