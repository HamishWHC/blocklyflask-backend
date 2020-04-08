from flask import jsonify

NOT_IMPLEMENTED = jsonify("Not yet implemented."), 501
NOT_FOUND = jsonify("That resource does not exist."), 404
FORBIDDEN = jsonify("You are forbidden to access this resource."), 403
UNAUTHORIZED = jsonify("You must be authorized to access this resource."), 401