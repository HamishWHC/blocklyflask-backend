from app import marshmallow
from marshmallow import fields, validate
from app.models import User


class UserSchema(marshmallow.ModelSchema):
    class Meta:
        model = User
        fields = ("id", "email", "projects", "username")
    
    id = fields.Integer(dump_only=True)
    email = fields.String(required=True, validate=validate.Regexp(r"^[^@]+@[^@]+\.[^@]+$"))
    username = fields.String(required=True)
    projects = fields.Nested("ProjectSchema", exclude=("user", ), many=True, dump_only=True)
