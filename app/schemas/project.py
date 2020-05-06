from marshmallow import fields, validate

from app import marshmallow
from app.models import Project


class ProjectSchema(marshmallow.ModelSchema):
    class Meta:
        model = Project
        fields = ("id", "user", "name", "last_modified", "root_directory")

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=6, max=60))
    last_modified = fields.DateTime(dump_only=True)
    user = fields.Nested("UserSchema", exclude=("projects",), dump_only=True)
    root_directory = fields.Nested("DirectorySchema", exclude=("project", "parent"), dump_only=True)
