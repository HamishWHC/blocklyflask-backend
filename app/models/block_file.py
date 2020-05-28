from app import db
from app.models import Project


class BlockFile(db.Model):
    __tablename__ = "block_files"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True)
    directory_id = db.Column(db.Integer, db.ForeignKey("directories.id"))
    block_xml = db.Column(db.Text())
    # project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))

    directory = db.relationship("Directory", backref=db.backref("block_files", cascade="all, delete-orphan"))
    # project = db.relationship("Project", backref=db.backref("block_files", cascade="all, delete-orphan"))

    def _full_path(self, is_end: bool = False) -> str:
        return self.directory._full_path(is_end=False) + self.name + ("/" if is_end else "")

    @property
    def full_path(self) -> str:
        return self.directory.full_path + "/" + self.name

    @property
    def project(self) -> Project:
        return self.directory.project
