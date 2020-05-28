from app import db


class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)
    email = db.Column(db.String(60), unique=True, index=True)
    hashed_password = db.Column(db.String())
