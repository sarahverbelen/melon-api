import werkzeug

class NoEmailException(werkzeug.exceptions.HTTPException):
    code = 400
    description = 'Email is required'

class InvalidEmailException(werkzeug.exceptions.HTTPException):
    code = 400
    description = 'Email is invalid'