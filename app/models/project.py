from app import db


class Project(db.Model):
    __tablename__ = "projects"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    last_modified = db.Column(db.DateTime)
    root_directory_id = db.Column(db.Integer, db.ForeignKey("directories.id"))
    
    user = db.relationship("User", backref=db.backref("projects", cascade="all, delete-orphan"))
    root_directory = db.relationship("Directory", backref="_project", cascade="all, delete-orphan", single_parent=True)

    @property
    def block_files(self):
        return self.root_directory.all_block_files
