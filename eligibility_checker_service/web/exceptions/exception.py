class PythonFlaskBaseException(Exception):
    """Base exception for python flask app"""
    def __init__(self, msg=None):
        if not msg:
            msg = 'An uncaught error occourecd'


class InvalidSchema(PythonFlaskBaseException):
    """Exception for an invalid schema"""
    def __init__(self, msg=None):
        msg = msg if msg else 'Invalid Schema'
        super(InvalidSchema, self).__init__(msg=msg)
