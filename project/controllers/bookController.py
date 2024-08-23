from flask import Blueprint, jsonify, request
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from models.models import Book, Feedback, RentRequest
from settings.db_config import db
from utils.utils import *
from utils.validator import book_validator


book_bp = Blueprint('book_bp', __name__)


def bookSerializer(book):
    return {
        'id': book.id,
        'name': book.name,
        'content': book.content,
        'published_on': book.issue_date,
        'return_date': book.return_date,
        'authors': book.authors,
        'user_id': book.user_id
    }


def bookListSerializer(books):
    print(books)
    serialized_books = []
    for book in books:
        serialized_books.append({
            'id': book.id,
            'name': book.name,
            'content': book.content,
            'published_on': book.issue_date,
            'return_date': book.return_date,
            'authors': book.authors,
            'section': {
                'section_id': book.section.id,
                'section_name': book.section.name
            }
        })

    return serialized_books

SERVER_ERROR = "Server could't be able to process this request"


# Route to get all the books
@book_bp.get("/")
def get_books():

    try:
        books = Book.query.all()
        serialized_books = bookListSerializer(books)

        return jsonify(status='success', data=serialized_books), 200
    except Exception as e:
        print(e)
        error_resp = generate_error_response(SERVER_ERROR)
        return jsonify(error_resp), 500
    

# Route to get an individual book based on its id
@book_bp.get("/<string:id>")
def particular_book(id):

    try:
        book = Book.query.get(id)
        if book:
            serialized_book = bookSerializer(book)
            return jsonify(status='success', data=serialized_book), 200
        else:
            error_resp = generate_error_response("No book found")
            return jsonify(error_resp), 404
    except:
        error_resp = generate_error_response("Server Error")
        return jsonify(error_resp), 500


# Route to request the book for renting
@book_bp.get('/rent/<string:book_id>')
@jwt_required()
def rent_book(book_id):

    claims = get_jwt()
    user_id = claims['id']
    try:
        # Check if the user has already requested the book
        isduplicate = RentRequest.query.filter_by(book_id=book_id, user_id=user_id).first()

        if isduplicate:
            return jsonify(status='fail', error="you've already requested this book"), 400
        rent_request = RentRequest(user_id=user_id, book_id=book_id)

        # If it is a new request commit to database
        db.session.add(rent_request)
        db.session.flush()
        db.session.commit()

        return jsonify(status='success', message='Request sent to the librarian')

    except Exception as e:
        print(e)
        error_resp = generate_error_response("Server error")
        return jsonify(error_resp), 500


# Route to create the book (admin only)
@book_bp.get("/create")
@jwt_required()
def create_book():

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

        # Extract the data from the request
        data = request.args
        if 'name' in data and 'content' in data and 'authors' in data and 'section_id' in data:

            name = data['name']
            content = data['content']
            authors = data['authors']
            section_id = data['section_id']


            # Extra validation
            hasError = book_validator(name=name, content=content, authors=authors, section_id=section_id)
            if hasError is not None:
                return jsonify(hasError), 400

            # Create a book instance if there is no error
            book = Book(name=name, content=content, authors=authors, section_id=section_id)
            db.session.add(book)
            db.session.flush()
            db.session.commit()

            serialized_book = bookSerializer(book)
            return jsonify(status='success', data=serialized_book), 201
        
        else:
            error_resp = generate_error_response("Invalid inputs")
            return jsonify(error_resp), 400
        
    except Exception as e:
        print(e)
        error_resp = generate_error_response("Couldn't create book, try again")
        return jsonify(error_resp), 500
    

# Route for updating the book
@book_bp.put("/<string:id>")
@jwt_required()
def edit_book(id):

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

        # Extracting the data from the request
        data = request.json
        book = Book.query.get(id)


        if not book:
            error_resp = generate_error_response("No book found to edit")
            return jsonify(error_resp), 404

        # Validating the request data

        if 'name' in data:
            if len(data['name']) != 0:
                book.name = data['name']
        if 'content' in data:
            if len(data['content']) != 0:
                book.content = data['content']
        if 'section_id' in data:
            book.section_id = data['section_id']
        if 'authors' in data:
            if len(data['authors']) != 0:
                book.authors = data['authors']
        if 'published_on' in data:
            date_format = "%Y-%m-%d"
            book.issue_date = datetime.strptime(data['published_on'], date_format).date()

        db.session.add(book)
        db.session.flush()
        db.session.commit()

        book = bookSerializer(book)
        return jsonify(status='success', data=book)
    
    except Exception as e:
        print(e)
        error_resp = generate_error_response("Server error")
        return jsonify(error_resp), 500



# Route for deleting the book
@book_bp.delete("/<string:id>")
@jwt_required()
def delete_book(id):

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
        book = Book.query.get(id)
        if book:
            db.session.delete(book)
            db.session.commit()

            return jsonify(status='success'), 204
        else:
            error_resp = generate_error_response("No book found to be deleted")
            return jsonify(error_resp), 404
    except Exception as e:
        error_resp = generate_error_response("Server Error")
        return jsonify(error_resp), 500
    

# Route to post feedback   
@book_bp.post("/feedback/<string:book_id>")
@jwt_required()
def post_feedback(book_id):

    claims = get_jwt()
    user_id = claims['id']

    try:
        if not 'content' in request.json:
            error_resp = generate_error_response("feedback content should not be empty")
            return jsonify(error_resp), 400
        
        content = request.json.get("content")

        feedback = Feedback(user_id=user_id, book_id=book_id, content=content)

        db.session.add(feedback)
        db.session.flush()
        db.session.commit()

        return jsonify(status='success'), 201
    
    except Exception as e:
        print(e)
        error_resp = generate_error_response("Server Error")
        return jsonify(error_resp), 500


def feedback_serializer(feedbacks):
    serialized_feedbacks = []
    for feedback in feedbacks:
        serialized_feedbacks.append({
            'user_id': feedback.user_id,
            'content': feedback.content
        }) 

    return serialized_feedbacks


# Route to get feedbacks
@book_bp.get("/feedback/<string:book_id>")
@jwt_required()
def get_feedbacks(book_id): 
    try:
        feedbacks = Feedback.query.filter_by(book_id=book_id).all()
        serialized_feedbacks = feedback_serializer(feedbacks)

        return jsonify(status='success', data=serialized_feedbacks)
    except Exception as e:
        error_resp = generate_error_response("Server Error")
        return jsonify(error_resp), 500
    

# Route to return the requested book
@book_bp.get("/<string:book_id>/return")
@jwt_required()
def return_book(book_id):

    try:
        book = Book.query.get(book_id)
        claims = get_jwt()

        if book.user_id == claims['id']:
            book.user_id = None
            db.session.add(book)
            db.session.flush()
            db.session.commit()
            return jsonify(status='success', data='successfully returned')

        else:
            return jsonify(status='fail', error='You havent rented this book'), 400
    except Exception as e:
        print(e)
        error_response = generate_error_response('sever error')
        return jsonify(error_response), 500
    


@book_bp.get("/rented_books")
@jwt_required()
def get_rented_books():

    claims = get_jwt()

    if not 'id' in claims:
        error_resp = generate_error_response("Not a valid token")
        return jsonify(error_resp), 400

    try:
        books = Book.query.filter(Book.user_id==claims['id']).all()
        serialized_books = bookListSerializer(books)

        return jsonify(status='success', data=serialized_books), 200
    except Exception as e:
        print(e)
        error_resp = generate_error_response(e)
        return jsonify(error_resp), 500    