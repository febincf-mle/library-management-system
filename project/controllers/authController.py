from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask import request, Blueprint, jsonify
from app import bcrypt

from models.models import *
from settings.db_config import db

from utils.validator import authentication_validator


auth = Blueprint('auth', __name__)



def serialize_users(users):
    serialized_users = []
    for user in users:
        serialized_users.append({
            'id': user.id,
            'username': user.username,
        })
    return serialized_users


@auth.get("/")
@jwt_required()
def users():

    users = User.query.all()
    serialized_users = serialize_users(users)

    return jsonify({
        'status': 'success',
        'body': serialized_users,
    })
    


@auth.post("/signup")
def signup():

    data = request.get_json()


    # Validating the credentials

    if 'username' not in data or \
        'email' not in data or \
            'password' not in data:
        return jsonify({ 'status': 'failed', 'error': 'Invalid credentials' }), 400
    
    
    username = data['username']
    email = data['email']
    password = data['password']
    address = ""

    # Extra validation
    hasError = authentication_validator(email, password, username)

    # check if there is any error
    if hasError is not None:
        return jsonify(hasError), 400


    if 'address' in data:
        address = data['address']

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, email=email, password=hashed_password, address=address)

    try:
        db.session.add(user)
        db.session.flush()
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({ 'status': 'failed', 'error': 'Server Error' }), 500
    else:
        return jsonify({ 'status': 'success' }), 201


@auth.post("/login")
def login():

    data = request.get_json()


    # Check for any bad request
    if 'email' not in data or 'password' not in data:
        return { 'status': 'failed', 'error': 'Invalid credentials' }, 400

    email = data['email']
    password = data['password']


    # Extra validation
    hasError = authentication_validator(email, password)

    # Check if the extra validation has any error
    if hasError is not None:
        return jsonify(hasError), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({ 'status': 'failed', 'error': 'Not a Valid user' }), 400
    isValidPassword = bcrypt.check_password_hash(user.password, password)

    if isValidPassword:
        # Using additional required information
        additional_claims = {
            'id': user.id,
            'role': user.role
        }

        # Updating the user last_seen to the login time
        user.last_seen = datetime.now().date()
        db.session.add(user)
        db.session.flush()
        db.session.commit()

        access_token = create_access_token(identity=email, additional_claims=additional_claims)
        return jsonify({
            'status': 'success',
            'token': access_token,
            'user': {
                'id': user.id,
                'role': user.role
            }
        })
    
    return jsonify({ 'status': 'failed', 'error': 'Not a Valid password' }), 400