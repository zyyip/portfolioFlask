import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class users(db.Model):
    __tablename__ = "users"
    userID = db.Column(db.Integer, nullable=False, primary_key=True)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    pwd = db.Column(db.String, nullable=False)
    lastLogin = db.Column(db.DateTime, nullable=True)
    portfolio = db.Column(db.String, nullable=True)
    
class resumecount(db.Model):
    __tablename__="resumecount"
    resumecountid= db.Column(db.Integer, nullable=False, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey("users.userID"), nullable=False)
    downloadDate = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)


class feedbackcount(db.Model):
    __tablename__= "feedbackcount"
    feedbackid= db.Column(db.Integer, nullable=False, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey("users.userID"), nullable=False)
    feedbackdate = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    contact_name = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    descriptions = db.Column(db.String, nullable=False)
    response = db.Column(db.String, nullable=False)



# class Books(db.Model):
#     __tablename__ = "resumeCount"
#     resumeCountID = db.Column(db.Integer, nullable=False, primary_key=True)
#     userID = db.Column(db.Integer,db.ForeignKey("Users.userid"), nullable=False)
#     downloadDate = db.Column(db.Timestamp, nullable=False)



# class Bookreview(db.Model):
#     __tablename__ = "bookreviews"
#     reviewid = db.Column(db.Integer, primary_key=True)
#     review_details = db.Column(db.String, nullable=False)
#     review_rating = db.Column(db.Integer, nullable=False)
#     reviewer_fname = db.Column(db.String, nullable=False)
#     reviewer_lname = db.Column(db.String, nullable=False)
#     userid = db.Column(db.String, db.ForeignKey("Users.userid"), nullable=False)
#     isbn = db.Column(db.String, db.ForeignKey("Books.isbn"), nullable=False)
