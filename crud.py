"""CRUD operations"""

from model import db, User, InfantVaccine, AdolescentVaccine, AdultVaccine, Profile, connect_to_db

def create_user(email, password, name):
    """Create and return new user"""

    user = User(email=email, password=password, name=name)

    return user

def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()


def create_infant_vaccine(Vaccine, Birth, month_one, month_two, month_four, month_six, month_nine, month_twelve, month_fifteen):
    """Creates and returns new vaccine"""

    infant_vaccine = InfantVaccine(Vaccine=Vaccine,
                       Birth=Birth,
                       month_one=month_one,
                       month_two=month_two,
                       month_four=month_four,
                       month_six=month_six,
                       month_nine=month_nine,
                       month_twelve=month_twelve,
                       month_fifteen=month_fifteen)
    return infant_vaccine

def create_adolescent_vaccine(Vaccine, month_eighteen, month_nineteen, two_to_four, four_to_six, seven_to_ten, eleven_to_twelve, thirteen_to_fifteen, sixteen, seventeen_to_eighteen):
    """Creates and returns new vaccine"""

    adolescent_vaccine = AdolescentVaccine(Vaccine=Vaccine,
                       month_eighteen=month_eighteen,
                       month_nineteen=month_nineteen,
                       two_to_four=two_to_four,
                       four_to_six=four_to_six,
                       seven_to_ten=seven_to_ten,
                       eleven_to_twelve=eleven_to_twelve,
                       thirteen_to_fifteen=thirteen_to_fifteen,
                       sixteen=sixteen,
                       seventeen_to_eighteen=seventeen_to_eighteen)
    return adolescent_vaccine

def create_vaccine(Vaccine, nineteen_to_twentysix, twentyseven_to_fortynine, fifty_to_sixtyfour, sixtyfive):
    """Creates and returns new vaccine"""

    adult_vaccine = AdultVaccine(Vaccine=Vaccine,
                       nineteen_to_twentysix=nineteen_to_twentysix,
                       twentyseven_to_fortynine=twentyseven_to_fortynine,
                       fifty_to_sixtyfour=fifty_to_sixtyfour,
                       sixtyfive=sixtyfive)
    return adult_vaccine

def create_profile(user, name, age, vaccine_status):
    """Creates and returns new profile"""

    profile = Profile(user=user, name=name, age=age, vaccine_status=vaccine_status)

    return profile

if __name__ == '__main__':
    from server import app
    connect_to_db(app)