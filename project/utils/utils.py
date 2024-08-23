def generate_error_response(message):
    return {
        'status': 'fail',
        'error': message
    }