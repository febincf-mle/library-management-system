from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt


from datetime import datetime, timedelta

from .bookController import bookSerializer
from models.models import Book, RentRequest, User
from utils.utils import generate_error_response
from settings.db_config import db



librarian_bp = Blueprint("librarian_bp", __name__)


# Route to get all the pending book requests
@librarian_bp.get("/book_requests")
@jwt_required()
def book_requests():

    ### jwt verification ###

    claims = get_jwt()

    if 'role' in claims:
        if not claims['role'] == 'admin':
            error_resp = generate_error_response("You are not authorized to this")
            return jsonify(error_resp), 403
    else:
        error_resp = generate_error_response("Not a valid token")
        return jsonify(error_resp), 400

    try:
        rent_requests = RentRequest.query.all()
        detailed_rent_requests = []

        # serializing the rent requests
        for request in rent_requests:
            user = User.query.get(request.user_id)
            book = Book.query.get(request.book_id)


            detailed_rent_requests.append({
                'user': {
                    'id': user.id,
                    'name': user.username
                },

                'book': bookSerializer(book)
            })


        return jsonify(status='success', data=detailed_rent_requests), 200
    except Exception as e:
        print(e)
        error_resp = generate_error_response("Server error")
        return jsonify(error_resp), 500
    

# Route to accept the rent request of the users
@librarian_bp.post("/rent")
@jwt_required()
def issue_book():

    ### jwt verification ###

    claims = get_jwt()

    if 'role' in claims:
        if not claims['role'] == 'admin':
            error_resp = generate_error_response("You are not authorized to this")
            return jsonify(error_resp), 403
    else:
        error_resp = generate_error_response("Not a valid token")
        return jsonify(error_resp), 400
    
    try:

        data = request.json
        if 'user_id' in data and 'book_id' in data:
            book_id, user_id = data['book_id'], data['user_id']

            book = Book.query.get(book_id)
            user = User.query.get(user_id)

            # Check if the book is valid and available
            if book is None:
                error_resp = generate_error_response("No book found")
                return jsonify(error_resp), 404
            
            # Check if the user is valid
            if user is None:
                error_resp = generate_error_response("Not a valid user"), 400

            # check if the book is already rented by other users
            if book.user_id is not None:
                return jsonify(status='failed', error='already rented by other user')
            
            # check if the user has rented more than 5 books
            if len(user.rented_books) >=5:
                return jsonify(status='fail', error='cannot rent more than 5 books')

            book.user_id = user_id
            # applying the return date for the book
            book.return_date = datetime.utcnow() + timedelta(days=1) 

            db.session.add(book)
            db.session.flush()
            db.session.commit()

            # clean up
            rent_request =  RentRequest.query.filter_by(user_id=user_id, book_id=book_id).first()
            db.session.delete(rent_request)
            db.session.commit()

            return jsonify(status='success'), 201
        
        else:
            error_resp = generate_error_response("Not a valid request")
            return jsonify(error_resp), 400
        
    except Exception as e:
        print(e)
        db.session.rollback()
        error_resp = generate_error_response("server error")
        return jsonify(error_resp), 500
    

# Route to get all the book which has been rented
@librarian_bp.get("/rented_books")
@jwt_required()
def rented_books():

    ### jwt authentication ###

    claims = get_jwt()

    if 'role' in claims:
        if not claims['role'] == 'admin':
            error_resp = generate_error_response('Only admin can use this service')
            return jsonify(error_resp), 401
    else:
        return jsonify(status='fail', error='Not a valid token'), 400

    try:
    
        books_rented = Book.query.filter(Book.user_id.isnot(None)).all()

        serialized_books_rented = []
        for book in books_rented:
            # Query the user information associated with the book
            user = User.query.get(book.user_id)

            serialized_books_rented.append({
                'book': {
                    'id': book.id,
                    'name': book.name,
                    'return_date': book.return_date
                },
                'user': {
                    'id': user.id,
                    'username': user.username
                }
            })

        return jsonify(status='success', data=serialized_books_rented), 200
    
    except Exception as e:
        print(e)
        error_resp = generate_error_response('server error')
        return jsonify(error_resp), 500


# Route to revoke permission of using book from the user
@librarian_bp.delete("/<string:book_id>/revoke/<string:user_id>")
@jwt_required()
def revoke_permission(book_id, user_id):

    #### jwt authentication ###

    claims = get_jwt()

    if 'role' in claims:
        if not claims['role'] == 'admin':
            error_resp = generate_error_response('Only admin can use this service')
            return jsonify(error_resp), 401
    else:
        return jsonify(status='fail', error='Not a valid token'), 400
    

    try:
        book = Book.query.get(book_id)
        user = User.query.get(user_id)

        if user is None:
            error_resp = generate_error_response("Not a valid user")
            return jsonify(error_resp), 401

        if book and (int(book.user_id) == int(user_id)):

            book.user_id = None
            book.return_date = None

            db.session.add(book)
            db.session.flush()
            db.session.commit()

            return jsonify(status='success', message='successfully revoked'), 204
        else:
            return jsonify(status='fail', error='Bad request or invalid credentials'), 400
    except Exception as e:
        print(e)
        error_resp = generate_error_response("server error")
        return jsonify(error_resp), 500


# Route to reject the rent request of the user
@librarian_bp.delete("/rent_request/<string:book_id>/user/<string:user_id>")
@jwt_required()
def delete_request(book_id, user_id):

    #### jwt authentication ###

    claims = get_jwt()

    if 'role' in claims:
        if not claims['role'] == 'admin':
            error_resp = generate_error_response('Only admin can use this service')
            return jsonify(error_resp), 401
    else:
        return jsonify(status='fail', error='Not a valid token'), 400
    

    try:
        rent_request = RentRequest.query.filter_by(user_id=user_id, book_id=book_id).first()

        if rent_request:
            db.session.delete(rent_request)
            db.session.commit()
            return jsonify(status='success', message='successfully deleted the request'), 204
        else:
            return jsonify(status='fail', error='Bad request or invalid credentials'), 400
    except Exception as e:
        print(e)
        error_resp = generate_error_response("server error")
        return jsonify(error_resp), 500