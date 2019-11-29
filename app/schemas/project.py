from app import marshmallow
from marshmallow import fields, validate
from app.models import Project


class ProjectSchema(marshmallow.ModelSchema):
    class Meta:
        model = Project
        fields = ("id", "user", "name", "last_modified", "files")
    
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(60))
    last_modified = fields.DateTime(dump_only=True)
    user = fields.Nested("UserSchema", exclude=("projects",), dump_only=True)
    files = fields.Nested("BlockFileSchema", excludes=("project",), dump_only=True)
