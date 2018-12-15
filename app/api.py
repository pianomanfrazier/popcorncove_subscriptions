from flask import Blueprint, jsonify, request
import hashlib
from .authentication import requires_auth
from .models import Customer
from . import db

api = Blueprint('api', __name__)

@api.route('/', methods=['GET'])
def index():
    return jsonify({'msg': 'Popcorn Cove Subscriptions version 1'})
