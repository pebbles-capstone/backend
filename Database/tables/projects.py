from Database.database import db

class Projects(db.Model):
    projectID = db.Column(db.Int, primary_key=True)
    supervisorID = db.Column(db.Int, db.ForeignKey("professors.supervisorID"))
    title = db.Column(db.String)
    description = db.Column(db.String)
    tags = db.Column(db.String)