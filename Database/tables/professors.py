from Database.database import db

class Professors(db.Model):
    supervisorID = db.Column(db.Int, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    interestVector = db.Column(db.String) 