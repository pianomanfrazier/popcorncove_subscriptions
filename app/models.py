from flask import abort
import hashlib
from datetime import datetime
from . import db
from . import app
from sqlalchemy.sql import func

class Customer(db.Model):
  __tablename__            = 'customer'
  id                       = db.Column(db.Integer, primary_key=True)
  name                     = db.Column(db.String(70), index=True, nullable=False)
  phone                    = db.Column(db.String(25), index=True, nullable=False)
  email                    = db.Column(db.String(255), index=True, nullable=False)
  preferredShippingAddress = db.Column(db.Integer, db.ForeignKey('shippingaddress.id'))
  time_created             = db.Column(db.DateTime(timezone=True), server_default=func.now()) 

  def __repr__(self):
    return '<Customer {}>'.format(self.name)

  def to_dict(self):
    return {
      'id': self.id,
      'name': self.name,
      'phone': self.phone,
      'email': self.email,
      'preferredShippingAddress': self.preferredShippingAddress,
      'time_created': self.time_created
    }
  
  def from_dict(self, data):
    preferredShippingAddress = None
    if 'preferredShippingAddress' in data.keys():
      preferredShippingAddress = data['preferredShippingAddress']
    try:
      self.name                     = data['name']
      self.phone                    = data['phone']
      self.email                    = data['email']
      self.preferredShippingAddress = preferredShippingAddress
    except KeyError:
      abort(400)

class Subscription(db.Model):
  __tablename__     = 'subscription'
  id                = db.Column(db.Integer, primary_key=True)
  customerID        = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False) 
  itemID            = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False) 
  shippingAddressID = db.Column(db.Integer, db.ForeignKey('shippingaddress.id'), nullable=False)
  startDate         = db.Column(db.Date, nullable=False)
  stopDate          = db.Column(db.Date, nullable=False)
  note              = db.Column(db.String(255))

  def __repr__(self):
    return '<Subscription {}>'.format(self.id)

  def to_dict(self):
    startDate = self.startDate.strftime('%Y-%m')
    stopDate = self.stopDate.strftime('%Y-%m')
    return {
      'id'                : self.id,
      'customerID'        : self.customerID, 
      'itemID'            : self.itemID,
      'shippingAddressID' : self.shippingAddressID,
      'startDate'         : startDate,
      'stopDate'          : stopDate,
      'note'              : self.note
    }
  
  def from_dict(self, data):
    if ('note' in data.keys()):
      self.note = data['note']
    try:
      startDate              = datetime.strptime(data['startDate'], '%Y-%m')
      stopDate               = datetime.strptime(data['stopDate'], '%Y-%m')
      self.customerID        = data['customerID'] 
      self.itemID            = data['itemID'] 
      self.shippingAddressID = data['shippingAddressID'] 
      self.startDate         = startDate
      self.stopDate          = stopDate
    except KeyError:
      abort(400)


class Item(db.Model):
  __tablename__ = 'item'
  id            = db.Column(db.Integer, primary_key=True)
  name          = db.Column(db.String(25))

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
  customerID    = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False) 
  address       = db.Column(db.String(100), nullable=False)
  city          = db.Column(db.String(40), nullable=False)
  state         = db.Column(db.String(40), nullable=False)
  zip           = db.Column(db.String(11), nullable=False)

  def __repr__(self):
    return '<ShippingAddress {}>'.format(self.address)

  def to_dict(self):
    return {
      'id'           : self.id,
      'customerID'   : self.customerID, 
      'address'      : self.address, 
      'city'         : self.city, 
      'state'        : self.state, 
      'zip'          : self.zip
    }
  
  def from_dict(self, data):
    try:
      self.customerID    = data['customerID'] 
      self.address       = data['address'] 
      self.city          = data['city'] 
      self.state         = data['state'] 
      self.zip           = data['zip'] 
    except KeyError:
      abort(400)
