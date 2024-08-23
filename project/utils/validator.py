def generate_error_message(message):
    return {
        'status': 'fail',
        'error': message
    }


def authentication_validator(email, password, username=None):
    
    # If username is passed here then it is a signup
    if username is not None:
        if len(username) == 0:
            return generate_error_message('Username cannot be empty')
        
    if len(email) <=6 or ('@' not in email):
        return generate_error_message('Please provide a valid email')
    

    return None


def book_validator(name, content, authors, section_id):

    if len(name) == 0:
        return generate_error_message('Name of the book cannot be empty')
    
    if len(content) == 0:
        return generate_error_message('Content of the book cannot be empty')
    
    if len(authors) <= 3:
        return generate_error_message('please provide a valid author')
    
    try:
        section_id_ISVALID = int(section_id)
    except:
        return generate_error_message("Not a valid section")
    
    return None
    

def section_validator(name, description):

    if len(name) == 0:
        return generate_error_message("Section name cannot be empty")
    
    if len(description) == 0:
        return generate_error_message('Description of a section cannot be empty')
    
    return None