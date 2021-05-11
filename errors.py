import werkzeug

class NoEmailException(werkzeug.exceptions.HTTPException):
    code = 400
    description = 'Email is required'

class NoPasswordException(werkzeug.exceptions.HTTPException):
    code = 400
    description = 'Password is required'

class WrongPasswordException(werkzeug.exceptions.HTTPException):
    code = 403
    description = 'The provided password is not correct'

class UnauthorizedException(werkzeug.exceptions.HTTPException):
    code = 401
    description = 'You need to be logged in to do this.'

class InvalidEmailException(werkzeug.exceptions.HTTPException):
    code = 400
    description = 'Email is invalid'

class NotFoundException(werkzeug.exceptions.HTTPException):
    code = 404
    description = 'Requested resource was not found'