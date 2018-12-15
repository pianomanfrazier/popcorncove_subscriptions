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

class Subscription(db.Model):
  __tablename__     = 'subscription'
  id                = db.Column(db.Integer, primary_key=True)
  customerID        = db.Column(db.Integer, db.ForeignKey('customer.id')) 
  itemID            = db.Column(db.Integer, db.ForeignKey('item.id')) 
  shippingAddressID = db.Column(db.Integer, db.ForeignKey('shippingaddress.id'))
  startDate         = db.Column(db.Date)
  stopDate          = db.Column(db.Date)
  note              = db.Column(db.String(255))

class Item(db.Model):
  __tablename = 'item'
  id          = db.Column(db.Integer, primary_key=True)
  name        = db.Column(db.String(25))

class ShippingAddress(db.Model):
  __tablename__ = 'shippingaddress'
  id            = db.Column(db.Integer, primary_key=True)
  customerID    = db.Column(db.Integer, db.ForeignKey('customer.id')) 
  address       = db.Column(db.String(100))
  city          = db.Column(db.String(40))
  state         = db.Column(db.String(40))
  zip           = db.Column(db.String(11))