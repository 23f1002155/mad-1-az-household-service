from werkzeug.exceptions import HTTPException
from flask import make_response


class Not_Found(HTTPException):
    def __init__(self, status_code):
        self.response = make_response("", status_code)