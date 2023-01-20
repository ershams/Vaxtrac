"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime
import psycopg2
from sqlalchemy import create_engine as ce
from sqlalchemy import engine
import pandas as pd

import crud
import model
import server

os.system('dropdb vaxtrac')
os.system('createdb vaxtrac')

model.connect_to_db(server.app)
model.db.create_all()

url = engine.URL.create(
    "postgresql",
    host = "localhost",
    database ="vaxtrac",
    username="postgres",
    password= "1234"
)
engine = ce(url)
# engine = ce('postgresql://postgres@localhost:5432/vaxtrac')

# conn = psycopg2.connect(
#     host = "localhost",
#     database ="vaxtrac",
#     user="postgres",
#     password= "1234"
# )

df = pd.read_html('https://www.cdc.gov/vaccines/schedules/hcp/imz/child-adolescent.html')


infant = df[1]
infant.set_index('Vaccine')
infant = infant.rename(columns={'Vaccine': 'infant_vaccine_name', 
                                'Birth': 'birth',
                                '1 mo': 'month_one',
                                '2 mos': 'month_two', 
                                '4 mos': 'month_four', 
                                '6 mos': 'month_six', 
                                '9 mos': 'month_nine', 
                                '12 mos': 'month_twelve',
                                '15 mos': 'month_fifteen'})

# birth_json = birth_to_month_fifteen.to_json(orient='index')
# # birth_object = json.dumps(birth_json, indent=9)
# with open('/home/ershams/src/vaxtrac2/birth_json_file', "r") as t:
#     vaccine_data = json.loads(t.read())
# print(infant)
# # print(type(birth_to_month_fifteen))

adolescent = df[2].drop(['4-6 yrs.1', '7-10 yrs.1', '17-18 yrs.1', '17-18 yrs.2'], axis=1)
adolescent.set_index('Vaccines')
adolescent = adolescent.rename(columns={'Vaccines': 'adolescent_vaccine_name', '18 mos': 'month_eighteen',
                                '19-23 mos': 'month_nineteen_to_twentyfour', 
                                '2-3 yrs': 'two_to_four', 
                                '4-6 yrs': 'four_to_six', 
                                '7-10 yrs': 'seven_to_ten', 
                                '11-12 yrs': 'eleven_to_twelve',
                                '13-15 yrs': 'thirteen_to_fifteen',
                                '16 yrs': 'sixteen',
                                '17-18 yrs': 'seventeen_to_eighteen'})

dataframe = pd.read_html('https://www.cdc.gov/vaccines/schedules/hcp/imz/adult.html')
adult_table = dataframe[0].drop(['19-26 years.1','19-26 years.2','27-49 years.1','27-49 years.2','27-49 years.3','50-64 years.1', '50-64 years.2', '50-64 years.3'], axis=1)
adult_table = adult_table.rename(columns={'Vaccine': 'adult_vaccine_name','19-26 years': 'nineteen_to_twentysix',
                                          '27-49 years': 'twentyseven_to_fortynine',
                                          '50-64 years': 'fifty_to_sixtyfour',
                                          '≥65 years' : 'sixtyfive'})

# merge = pd.concat([adolescent, infant], axis=1, join='outer')
# # print(merge)

# merge_again = pd.concat([merge, adult_table], axis=1, join='outer')
# print(merge_again)

vaccines_in_db = []

# for vaccine in vaccine_data:
#     birth, month_one, month_two, month_four, month_six, month_nine, month_twelve, month_fifteen = (vaccine["Vaccine"],
#           vaccine["Birth"], vaccine["month_one"], vaccine["month_two"],
#           vaccine["month_four"], vaccine["month_four"], vaccine["month_six"],
#           vaccine["month_nine"], vaccine["twelve"], vaccine["fifteen"],
#     )
# infant.to_sql('vaccines', engine, if_exists='append', index=False)
# adolescent.to_sql('vaccines', engine, if_exists='append', index=False)
# adult_table.to_sql('vaccines', engine, if_exists='append', index=False)
infant.to_sql('infant_vaccines', engine, if_exists='append', index=False)
adolescent.to_sql('adolescent_vaccines', engine, if_exists='append', index=False)
adult_table.to_sql('adult_vaccines', engine, if_exists='append', index=False)

# db_vaccine = crud.create_vaccine(Vaccine, Birth, month_one, month_two, month_four, month_six, month_nine, month_twelve, month_fifteen, month_eighteen, month_nineteen, two_to_four, four_to_six, seven_to_ten, eleven_to_twelve, thirteen_to_fifteen, sixteen, seventeen_to_eighteen, nineteen_to_twentysix, twentyseven_to_fortynine, fifty_to_sixtyfour, sixtyfive)
# vaccines_in_db.append(db_vaccine)

model.db.session.add_all(vaccines_in_db)
model.db.session.commit()
