from marshmallow import fields
from marshmallow.validate import Length

from app import marshmallow
from app.models import BlockFile, Directory
from app.utils import exists


class DirectorySchema(marshmallow.ModelSchema):
    class Meta:
        model = Directory
        fields = ("id", "project", "name", "parent", "parent_id", "full_path", "sub_directories", "block_files")

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=Length(min=1, max=255))
    parent = fields.Nested("DirectorySchema", exclude=("sub_directories",), dump_only=True)
    project = fields.Nested("ProjectSchema", exclude=("root_directory",), dump_only=True)
    sub_directories = fields.Nested("DirectorySchema", exclude=("parent", "project"), many=True, dump_only=True)
    parent_id = fields.Integer(required=True, validate=exists(Directory, "directory"), load_only=True)
    block_files = fields.Nested("BlockFileSchema", exclude=("directory", "project", "block_xml"), many=True)
    full_path = fields.String(dump_only=True)
