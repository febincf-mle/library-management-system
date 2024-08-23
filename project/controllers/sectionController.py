from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from datetime import datetime, date

from .bookController import bookListSerializer
from models.models import Section
from settings.db_config import db
from utils.utils import *
from utils.validator import section_validator

section_bp = Blueprint('section_bp', __name__)


def sectionSerializer(section):
    books = bookListSerializer(section.books)
    return {
        'id': section.id,
        'name': section.name,
        'description': section.description,
        'date_created': section.date_created,
        'books': books,
    }


def sectionListSerializer(sections):
    serialized_sections = []
    for section in sections:
        serialized_sections.append({
        'id': section.id,
        'name': section.name,
        'description': section.description,
        'date_created': section.date_created
    })

    return serialized_sections

SERVER_ERROR = "Server could't be able to process this request"


# Route to get all the available sections
@section_bp.get("/")
def get_sections():

    try:
        sections = Section.query.all()
        serialized_sections = sectionListSerializer(sections)

        return jsonify(status='success', data=serialized_sections), 200
    except Exception as e:
        error_resp = generate_error_response(SERVER_ERROR)
        return jsonify(error_resp), 500
    

# Route to get particular section based on id
@section_bp.get("/<string:id>")
def particular_section(id):

    try:
        section = Section.query.get(id)
        if section:
            serialized_section = sectionSerializer(section)
            return jsonify(status='success', data=serialized_section), 200
        else:
            error_resp = generate_error_response("No section found")
            return jsonify(error_resp), 404
    except:
        error_resp = generate_error_response("Server Error")
        return jsonify(error_resp), 500


# Route to create a new section
@section_bp.get("/create")
@jwt_required()
def create_section():

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
        data = request.args
        if 'name' in data and 'description' in data:

            name = data['name']
            description = data['description']

            # Extra validation
            hasError = section_validator(name, description)
            if hasError is not None:
                return jsonify(hasError), 404

            section = Section(name=name, description=description)
            
            db.session.add(section)
            db.session.flush()
            db.session.commit()

            serialized_section = sectionSerializer(section)
            return jsonify(status='success', data=serialized_section), 201
        
        else:
            error_resp = generate_error_response("Invalid inputs")
            return jsonify(error_resp), 400
        
    except Exception as e:
        error_resp = generate_error_response("Couldn't create section, try again")
        return jsonify(error_resp), 500
    

# Route to update the section
@section_bp.put("/<string:id>")
@jwt_required()
def edit_section(id):

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
        section = Section.query.get(id)

        if not section:
            error_resp = generate_error_response("No section found to edit")
            return jsonify(error_resp), 404

        if 'name' in data:
            if len(data['name']) != 0:
                section.name = data['name']
        if 'description' in data:
            if len(data['description']) != 0:
                section.description = data['description']
        if 'date_created' in data:
            date_format = "%Y-%m-%d"
            section.date_created = datetime.strptime(data['date_created'], date_format).date()

        db.session.add(section)
        db.session.flush()
        db.session.commit()

        serialized_section = sectionSerializer(section)
        return jsonify(status='success', data=serialized_section)
    
    except Exception as e:
        print(e)
        error_resp = generate_error_response("Server error")
        return jsonify(error_resp), 500


# Route to delete a particular section
@section_bp.delete("/<string:id>")
@jwt_required()
def delete_section(id):

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
        section = Section.query.get(id)
        if section:
            db.session.delete(section)
            db.session.commit()

            return jsonify(status='success'), 204
        else:
            error_resp = generate_error_response("No section found to be deleted")
            return jsonify(error_resp), 404
    except Exception as e:
        print(e)
        error_resp = generate_error_response("Server Error")
        return jsonify(error_resp), 500