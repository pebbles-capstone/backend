from Database.database import db

class Users(db.Model):
    userID = db.Column(db.Int, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    interestVector = db.Column(db.String)
    teamID = db.Column(db.Int)
