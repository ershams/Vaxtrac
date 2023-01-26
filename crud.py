"""CRUD operations"""

from model import db, User, InfantVaccine, AdolescentVaccine, AdultVaccine, CompletedIMZ, Eligibility, connect_to_db
import psycopg2

def create_user(email, password, name):
    """Create and return new user"""

    user = User(email=email, password=password, name=name)

    db.session.add(user)
    db.session.commit()

    return user

def get_user_by_id(user_id):
    """Return a user by primary key."""

    user = User.query.get(user_id)

    return user

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

def get_all_users():
    all_users = User.query.all()

    return all_users


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

# def get_infant_vaccine(infant_vaccine):
#     inf_vaccine = InfantVaccine.query.all()

#     inf_list = []

#     for item in infant_vaccine:
#         inf_list.append(item)

#     return inf_list

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

# def create_profile(user, name, age, gender):
#     """Creates and returns new profile"""

#     profile = Profile(user=user, name=name,  age=age, gender=gender)

#     return profile

# def get_profile_by_id(profile_id):
#     """Return a user by primary key."""

#     return Profile.query.get(profile_id)

def create_completed_imz(imz, admin_date, reaction, user_id):
    """Creates and returns new profile"""

    user = User.query.get(user_id)

    completed_imz = CompletedIMZ(imz=imz, admin_date=admin_date, reaction=reaction, user=user)

    return completed_imz

def get_user_vaccine():

    vaccine = db.session.query(CompletedIMZ.imz)

    return vaccine

def get_user_vaccine_date():

    date = db.session.query(CompletedIMZ.admin_date)
    
    return date

def get_user_vaccine_reaction():

    reaction = db.session.query(CompletedIMZ.reaction)
    
    return reaction


def create_eligibility(genderM, genderF, genderN, age, pregnantY, pregnantN, 
                                        travelY, travelN, chickenpoxY, chickenpoxN, chickenpoxU, 
                                        fluidsY, fluidsN, injectablesY, injectablesN):
    """Creates and returns new profile"""

    eligibility = Eligibility(gender=gender, age=age, pregnant=pregnant, travel=travel, chickenpox=chickenpox, fluids=fluids, injectables=injectables)

    return eligibility

def calculateAge(birthDate):
    days_in_month = 30.437   
    age = int((date.today() - birthDate).days / days_in_month)
    return age

def get_db_connection():
    conn = psycopg2.connect(
    host = "localhost",
    database ="vaxtrac",
    user="postgres",
    password= "1234")

    return conn

def inf_vacc_brith_to_one():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT infant_vaccine_name FROM Infant_Vaccines where birth is not null')
    vaccine_birth = cur.fetchall()
    cur.close()
    conn.close()

    return vaccine_birth

def inf_vacc_two_to_four():
    vaccine = InfantVaccine.query.filter(InfantVaccine.month_two != None)
    
    return vaccine

def inf_vacc_six_to_nine():
    vaccine = InfantVaccine.query.filter(InfantVaccine.month_six != None)
    
    return vaccine

def inf_vacc_tweleve_to_fifteen():
    vaccine = InfantVaccine.query.filter(InfantVaccine.month_twelve != None)
    
    return vaccine

def adol_vacc_mo_eighteen():
    vaccine = AdolescentVaccine.query.filter(AdolescentVaccine.month_eighteen != None)
    
    return vaccine

def adol_vacc_two():
    vaccine = AdolescentVaccine.query.filter(AdolescentVaccine.four_to_six != None)
    
    return vaccine

def adol_vacc_seven():
    vaccine = AdolescentVaccine.query.filter(AdolescentVaccine.seven_to_ten != None)
    
    return vaccine

def adol_vacc_eleven_to_eighteen():
    vaccine = AdolescentVaccine.query.filter(AdolescentVaccine.eleven_to_twelve != None)
    
    return vaccine

def adult_to_fortynine():
    vaccine = AdultVaccine.query.filter(AdultVaccine.twentyseven_to_fortynine != None)
    
    return vaccine

def adult_fifty_to_sixtyfive():
    vaccine = AdultVaccine.query.filter(AdultVaccine.fifty_to_sixtyfour != None)
    
    return vaccine

def adult_sixtyfive():
    vaccine = AdultVaccine.query.filter(AdultVaccine.sixtyfive != None)
    
    return vaccine

if __name__ == '__main__':
    from server import app
    connect_to_db(app)