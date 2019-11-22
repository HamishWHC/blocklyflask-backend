from app import db


class Project(db.Model):
    __tablename__ = "projects"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    last_modified = db.Column(db.DateTime)
    
    user = db.relationship("User", backref=db.backref("projects", cascade="all, delete-orphan"))
