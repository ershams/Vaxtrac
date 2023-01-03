from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = "user"
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    profiles = db.relationship("Profile", back_populates="user")

    def __repr__(self):
        return f'<"user"={self.user_id} "email"={self.email}>'

class Profile(db.Model):
    __tablename__ = "profile"

    profile_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, nullable = False)
    age = db.Column(db.DateTime, nullable = False)
    vaccine_status = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    # infant_vaccine_id = db.Column(db.Integer, db.ForeignKey("infant_vaccines.infant_vaccine_id"))
    # adolescent_vaccine_id = db.Column(db.Integer, db.ForeignKey("adolescent_vaccines.adolescent_vaccine_id"))
    # adult_vaccine_id = db.Column(db.Integer, db.ForeignKey("adult_vaccines.adult_vaccine_id"))

    user = db.relationship("User", back_populates="profiles")
    infant_vaccines = db.relationship("InfantVaccine", back_populates="profile")
    adolescent_vaccines = db.relationship("AdolescentVaccine", back_populates="profile")
    adult_vaccines = db.relationship("AdultVaccine", back_populates="profile")

    def __repr__(self):
        return f'<"user"={self.user_id}, "name"={self.name} "age"={self.age} "vaccine_status"={self.vaccine_status} "profile_id"={self.profile_id}>'

class InfantVaccine(db.Model):
    __tablename__ = "infant_vaccines"

    infant_vaccine_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    infant_vaccine_name = db.Column(db.String)
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.profile_id"))
    # Vaccine = db.Column(db.String, unique=True)
    birth = db.Column(db.String)
    month_one = db.Column(db.String)
    month_two = db.Column(db.String)
    month_four = db.Column(db.String)
    month_six = db.Column(db.String)
    month_nine = db.Column(db.String)
    month_twelve = db.Column(db.String)
    month_fifteen = db.Column(db.String)
    
    profile = db.relationship("Profile", back_populates="infant_vaccines")

class AdolescentVaccine(db.Model):
    __tablename__ = "adolescent_vaccines"

    adolescent_vaccine_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    adolescent_vaccine_name = db.Column(db.String)
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.profile_id"))
    # Vaccine = db.Column(db.String, unique=True)
    month_eighteen = db.Column(db.String)
    month_nineteen_to_twentyfour = db.Column(db.String)
    two_to_four = db.Column(db.String)
    four_to_six = db.Column(db.String)
    seven_to_ten = db.Column(db.String)
    eleven_to_twelve = db.Column(db.String)
    thirteen_to_fifteen = db.Column(db.String)
    sixteen = db.Column(db.String)
    seventeen_to_eighteen = db.Column(db.String)

    profile = db.relationship("Profile", back_populates="adolescent_vaccines")

class AdultVaccine(db.Model):
    __tablename__ = "adult_vaccines"

    adult_vaccine_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    adult_vaccine_name = db.Column(db.String)
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.profile_id"))
    nineteen_to_twentysix = db.Column(db.String)
    twentyseven_to_fortynine = db.Column(db.String)
    fifty_to_sixtyfour = db.Column(db.String)
    sixtyfive = db.Column(db.String)
    
    profile = db.relationship("Profile", back_populates="adult_vaccines")

def connect_to_db(flask_app, db_uri="postgresql:///vaxtrac", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)