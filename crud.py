"""CRUD operations"""

from model import db, User, InfantVaccine, AdolescentVaccine, AdultVaccine, CompletedIMZ, Eligibility, connect_to_db
import psycopg2
from bs4 import BeautifulSoup
import requests
from datetime import date, datetime

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

def get_eligibility_by_user(user_id): 
    
    return Eligibility.query.filter_by(user_id).one()

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

def create_completed_imz(imz, admin_date, reaction, user_id):
    """Creates and returns new profile"""

    user = User.query.get(user_id)

    completed_imz = CompletedIMZ(imz=imz, admin_date=admin_date, reaction=reaction, user=user)

    return completed_imz

def create_eligibility(genderM, genderF, genderN, age, pregnantY, pregnantN, 
                                        travelY, travelN, chickenpoxY, chickenpoxN, chickenpoxU, 
                                        fluidsY, fluidsN, injectablesY, injectablesN):
    """Creates and returns new profile"""

    eligibility = Eligibility(genderM=genderM, genderF=genderF, genderN=genderN, age=age, pregnantN=pregnantN, pregnantY=pregnantY, travelN=travelN, travelY=travelY, chickenpoxN=chickenpoxN, chickenpoxY=chickenpoxY, chickenpoxU=chickenpoxU, fluidsN=fluidsN, fluidsY=fluidsY, injectablesN=injectablesN, injectablesY=injectablesY)

    return eligibility

def calculate_age(age):
    cur_year = int((date.today()).strftime('%Y'))

    entered = datetime.strptime(age, '%Y-%m-%d')
    year = entered.year
    month = entered.month
    day = entered.day

    calc_age = ((((cur_year-year-1)*365.24 + (12 - month)*30.437 + day)/365))*12

    return calc_age

def get_recommended_vaccines(check_age):

    if check_age < 2:
        recommended = InfantVaccine.query.filter(InfantVaccine.birth != "")
    elif check_age < 6:
        recommended = InfantVaccine.query.filter(InfantVaccine.month_two != "")
    elif check_age < 12:
        recommended = InfantVaccine.query.filter(InfantVaccine.month_six != "")
    elif check_age < 18:
        recommended = InfantVaccine.query.filter(InfantVaccine.month_twelve != "")
    elif check_age < 24:
        recommended = AdolescentVaccine.query.filter(AdolescentVaccine.month_eighteen != "")
    elif check_age < 84:
        recommended = AdolescentVaccine.query.filter(AdolescentVaccine.four_to_six != "")
    elif check_age < 132:
        recommended = AdolescentVaccine.query.filter(AdolescentVaccine.seven_to_ten != "")
    elif check_age < 228:
        recommended = AdolescentVaccine.query.filter(AdolescentVaccine.eleven_to_twelve != "")
    elif check_age < 600:
        recommended = AdultVaccine.query.filter(AdultVaccine.twentyseven_to_fortynine != None)
    elif check_age < 780:
        recommended = AdultVaccine.query.filter(AdultVaccine.fifty_to_sixtyfour != "")
    else:
        recommended = AdultVaccine.query.filter(AdultVaccine.sixtyfive != "")

    return recommended


def get_pt_education(brandName):
   # brandName = data['results'][0]['brand_name']
    link = f'http://www.drugs.com/{brandName}.html'
    # print(link)

    # TODO check if in db else scrap site and add to db

    page1 = requests.get(link)
    education = BeautifulSoup(page1.content, 'html.parser')
    # print(education)

    success = education.find('h1').text 
    success = success != "Page Not Found" and success != "Forbidden"

    if education and success:
        uses = education.find('h2', {"id" : "uses"})
    
        if uses: 
            uses = uses.find_next_sibling('p').text

        warning = education.find('h2', id = "warnings")
        
        if warning:
            warning = warning.find_next_sibling('p').text

        # TODO add to database

        return {"uses" : uses, "warning" : warning}

# def get_pt_education(brandName):
#     # brandName = data['results'][0]['brand_name']
#     link = f'https://www.goodrx.com/{brandName}/what-is'
#     # print(link)

#     # TODO check if in db else scrap site and add to db

#     page1 = requests.get(link)
#     education = BeautifulSoup(page1.content, 'html.parser')
#     # print(education)

#     success = education.find('h2').text 
#     success = success != "Page Not Found" and success != "Forbidden"

#     if education and success:
#         uses = education.find(class_="class_name")
    
#         if uses: 
#             uses = uses.find_next_sibling('p').text

#         warning = education.find('h2', id = "warnings")
        
#         if warning:
#             warning = warning.find_next_sibling('p').text

#         # TODO add to database

#         return {"uses" : uses, "warning" : warning}

# def get_warnings(data):
#     brandName = data['results'][0]['brand_name']
#     link = f'https://www.drugs.com/{brandName}.html'

#     page1 = requests.get(link)
#     education = BeautifulSoup(page1.content, 'html.parser')
#     if education:
#         target = education.find('h2', text = "Warnings")
#         warnings = target.find_next_sibling('p').text

#         return warnings

if __name__ == '__main__':
    from server import app
    connect_to_db(app)