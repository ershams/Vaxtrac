from flask import Flask
app=Flask(__name__,template_folder='template')
import psycopg2
import requests
from pprint import pformat

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from model import connect_to_db, db, CompletedIMZ, User
import crud
import cloudinary.uploader
import os

os.system('source secrets.sh')

CLOUDINARY_KEY = os.environ['CLOUDINARY_KEY']
CLOUDINARY_SECRET = os.environ['CLOUDINARY_SECRET']
CLOUD_NAME = "dg9svgk9f"

from jinja2 import StrictUndefined

app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def homepage():
    """View homepage."""

    return render_template("homepage.html")

@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    # if request.method == 'POST':
    email = request.form.get("email")
    password = request.form.get("password")
    # print(email)
    # print(password)
    # # name = request.form.get("name")

    user = crud.get_user_by_email(email)
    print(user)
    if not user or user.password != password:
            flash("The email or password you entered was incorrect.")
    else:
            # Log in user by storing the user's email in session
            session["user_id"] = user.user_id
            flash(f"Welcome back, {user.name}!")

    return redirect("/dashboard")

@app.route("/logout")
def process_logout():
    """Log user out and clear the session."""

    del session["user_email"]
    return redirect("/") 

@app.route("/dashboard")
def show_dashboard():
    """Show user dashboard"""
   
    if 'user_email' in session:
        
        logged_in_email = session.get("user_email")
        user = crud.get_user_by_email(logged_in_email)
        

        # conn = get_db_connection()
        # cur = conn.cursor()
        # cur.execute('SELECT imz FROM completedimz where user is not null')
        # vaccine = cur.fetchall()
        # cur.close()
        # conn.close()

        # vaccine = db.session.query(CompletedIMZ.imz)
        # date = db.session.query(CompletedIMZ.admin_date)
        print(user)
        print(user.completedimzs)

        

    return render_template("dashboard.html")
    # return redirect ('/')

@app.route("/sign-up")
def show_sign_up_form():
    """take use to sign-up form"""
    return render_template("registration.html")

def get_db_connection():
    conn = psycopg2.connect(
    host = "localhost",
    database ="vaxtrac",
    user="postgres",
    password= "1234")

    return conn

@app.route("/quiz")
def show_quiz():
    """take use to sign-up form"""

    # conn = get_db_connection()
    # cur = conn.cursor()
    # cur.execute('SELECT * FROM Infant_Vaccines where birth is not null')
    # vaccine = cur.fetchall()
    # cur.close()
    # conn.close()
    # conn = get_db_connection()
    # cur = conn.cursor()
    # cur.execute('SELECT infant_vaccine_name FROM Infant_Vaccines where birth is not null or month_two is not null')
    # vaccine_one = cur.fetchall()
    # cur.close()
    # conn.close()
    # conn = get_db_connection()
    # cur = conn.cursor()
    # cur.execute('SELECT infant_vaccine_name FROM Infant_Vaccines where birth is not null or month_two is not null or month_four is not null')
    # vaccine_four = cur.fetchall()
    # cur.close()
    # conn.close()
   

    # vaccine = []

    # for items in vaccine_birth:
    #     if items not in vaccine:
    #         vaccine.append(items)

    # vacc_one_list = []

    # for items in vaccine_one:
    #     if items not in vacc_one_list:
    #         vacc_one_list.append(items)

    # vacc_four_list = []

    # for items in vaccine_four:
    #     if items not in vacc_four_list:
    #         vacc_one_list.append(items)

    # vaccine = InfantVaccine.query.filter(InfantVaccine.month_four != None)

    vaccine = crud.inf_vacc_two_to_four()

    vaccine_birth = []

    # for item in vaccine:
    #     if item not in vaccine_birth:
    #         vaccine_birth.append(item)

    return render_template("quiz.html", vaccine=vaccine)

@app.route("/registration", methods=["POST"])
def register_user():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")
    name = request.form.get("name")

    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
        # return redirect('/registration')
    else:
        user = crud.create_user(email, password, name)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")
        

    return redirect('/')

@app.route("/create_completed_imz", methods=["POST"])
def add_completed_imz():
    """log a new imz."""

    if 'user_id' not in session:
        return redirect("/")

    # user = crud.get_user_by_id(user_id)
    user_id = session.get('user_id')

    # user = User.query.get(user_id)

    imz = request.form.get('imzField')
    admin_date = request.form.get('adminDateField')
    reaction = request.form.get('reactionField')

    completed_imz = crud.create_completed_imz(imz, admin_date, reaction, user_id)

    db.session.add(completed_imz)
    db.session.commit()

    return redirect("/dashboard")

@app.route("/post-form-data", methods=["POST"])
def upload_image():
    my_file = request.files['my-file']

    result = cloudinary.uploader.upload(my_file,
                                        api_key = CLOUDINARY_KEY,
                                        api_secret = CLOUDINARY_SECRET,
                                        cloud_name = CLOUD_NAME)

    img_url = result['secure_url']
    return redirect ('/dashboard', img_url=img_url)    

@app.route("/eligible_imz", methods=["POST"])
def find_eligible_imz():
    """log a new imz."""

    gender = request.form.get('genderField')
    age = request.form.get('dobField')
    pregnant = request.form.get('pregnantField')
    travel = request.form.get('travelField')
    chickenpox = request.form.get('cpField')
    fluids = request.form.get('bloodField')
    injectables = request.form.get('injectField')

    eligibility = crud.create_eligibility(gender, age, pregnant, travel, chickenpox, fluids, injectables)

    db.session.add(eligibility)
    db.session.commit()

    return redirect("/dashboard")

@app.route("/add_vaccines")
def show_vaccines():

    return render_template ('/add_vaccines.html')

@app.route('/allvaccines/search')
def find_vaccines():
    """Search for vaccines"""

    brand_name = request.args.get('brand_name')

    
    url = 'https://api.fda.gov/drug/ndc.json'
    #pass in all search endpoints 
    payload = {'search': brand_name}


    response = requests.get(url, params=payload)
    data = response.json()
       
    if '_embedded' in data:
        vaccines = data['_embedded']['vaccines']
    else:
        vaccines = []

    return render_template('search-results.html',
                           pformat=pformat,
                           data=data,
                           results=vaccines)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
