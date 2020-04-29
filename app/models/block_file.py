from app import db


class BlockFile(db.Model):
    __tablename__ = "block_files"
    
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.Text())
    block_xml = db.Column(db.Text())
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))
    
    project = db.relationship("Project", backref=db.backref("block_files", cascade="all, delete-orphan"))
