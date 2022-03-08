from main import db
from werkzeug.security import generate_password_hash, check_password_hash
# import models
from datetime import date


class UserOluwatomilolaAdeniran(db.Model):  # notice  that  our  class  extends  db.Model
    __tablename__ = 'regusers'  # this  is  the  name  we  want  the  table  in  database  to  have.
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), unique=False, nullable=False)
    lastname = db.Column(db.String(20), unique=False, nullable=False)
    othernames = db.Column(db.String(20), unique=False, nullable=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(256), unique=False, nullable=False)

    #  represent  the  object  when  it  is  queried  for
    def __repr__(self):
        return '<Register  {}>'.format(self.id)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class ProduceOluwatomilolaAdeniran(db.Model):
    __tablename__ = 'fproduce'
    id = db.Column(db.Integer, primary_key=True)
    Produce_Name = db.Column(db.String(20), unique=False, nullable=False)
    Produce_Description = db.Column(db.String(100), unique=False, nullable=False)
    Photo_URL = db.Column(db.VARCHAR(2083), nullable=False)
    Weight = db.Column(db.Integer, unique=False, nullable=False)
    price_per_unit = db.Column(db.Float, unique=False, nullable=False)
    Quantity = db.Column(db.Integer, unique=False, nullable=False)


    def __repr__(self):
        return '<Produce {}>'.format(self.id)
