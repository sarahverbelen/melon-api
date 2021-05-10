import werkzeug

class NoEmailException(werkzeug.exceptions.HTTPException):
    code = 400
    description = 'Email is required'

class NoPasswordException(werkzeug.exceptions.HTTPException):
    code = 400
    description = 'Password is required'

class InvalidEmailException(werkzeug.exceptions.HTTPException):
    code = 400
    description = 'Email is invalid'

class NotFoundException(werkzeug.exceptions.HTTPException):
    code = 404
    description = 'Requested resource was not found'