from flask import Blueprint, request, jsonify
from models.models import Book, Section
from .bookController import bookListSerializer
from .sectionController import sectionListSerializer
from utils.utils import generate_error_response

search_bp = Blueprint("search_bp", __name__)


# Route to search for books
@search_bp.get("/")
def search_books():
    try:
        query = request.args.get("q")
        books = Book.query.filter(Book.name.like(f"%{query}%")).all()

        serializedBooks = bookListSerializer(books)
        return jsonify(status='success', data=serializedBooks), 200
    except Exception as e:
        error_resp = generate_error_response("server error")
        return jsonify(error_resp), 500
    

# Route to search for sections
@search_bp.get("/sections")
def search_sections():
    try:
        query = request.args.get("q")
        sections = Section.query.filter(Section.name.like(f"%{query}%")).all()

        serializedSections = sectionListSerializer(sections)
        return jsonify(status='success', data=serializedSections), 200
    except Exception as e:
        error_resp = generate_error_response("server error")
        return jsonify(error_resp), 500