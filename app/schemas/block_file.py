from marshmallow import fields
from marshmallow.validate import Length
from app import marshmallow
from app.models import Directory, BlockFile
from app.utils import exists


class BlockFileSchema(marshmallow.ModelSchema):
    class Meta:
        model = BlockFile
        fields = ("id", "name", "directory", "block_xml", "directory_id", "full_path", "project")

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=Length(min=1, max=255))
    block_xml = fields.String(required=False)
    directory = fields.Nested("DirectorySchema", exclude=("block_files",), dump_only=True)
    directory_id = fields.Integer(validate=[exists(Directory, "directory")], load_only=True)
    project = fields.Nested("ProjectSchema", exclude=("root_directory",), dump_only=True)
    full_path = fields.String(dump_only=True)
