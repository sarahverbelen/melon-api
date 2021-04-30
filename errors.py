import werkzeug

class NoEmailException(werkzeug.exceptions.HTTPException):
    code = 400
    description = 'Email is required'

class NoNameException(werkzeug.exceptions.HTTPException):
    code = 400
    description = 'Name is required'

class InvalidEmailException(werkzeug.exceptions.HTTPException):
    code = 400
    description = 'Email is invalid'