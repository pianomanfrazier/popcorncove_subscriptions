#!./venv/bin/python

from app import app, db
from app.models import Customer, Subscription, Item, ShippingAddress 

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Customer': Customer, 'Subscription': Subscription,
            'ShippingAddress': ShippingAddress, 'Item': Item}