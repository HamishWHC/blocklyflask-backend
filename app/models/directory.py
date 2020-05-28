from app import db
from typing import List
from app.models import Project, BlockFile


class Directory(db.Model):
    __tablename__ = "directories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("directories.id"))

    parent = db.relationship("Directory", backref=db.backref("sub_directories", cascade="all, delete-orphan"),
                             remote_side=[id])

    def _full_path(self, is_end: bool = False) -> str:
        if self.parent is None:
            return "/"
        else:
            return self.parent._full_path(is_end=False) + self.name + ("" if is_end else "/")

    @property
    def full_path(self) -> str:
        if self.parent is None:
            return "/"
        else:
            return self._full_path(is_end=True)

    @property
    def project(self) -> Project:
        if self.parent:
            return self.parent.project
        else:
            return self._project

    @property
    def all_block_files(self) -> List[BlockFile]:
        block_files = self.block_files
        for sub_dir in self.sub_directories:
            block_files.extend(sub_dir.all_block_files)
        return block_files
