from app import marshmallow
from marshmallow import fields, validate
from app.models import BlockFile


class BlockFileSchema(marshmallow.ModelSchema):
    class Meta:
        model = BlockFile
        fields = ("id", "project", "path", "block_xml")
    
    id = fields.Integer(dump_only=True)
    path = fields.String(required=True)
    block_xml = fields.String(required=False)
    project = fields.Nested("ProjectSchema", exclude=("files",), dump_only=True)
