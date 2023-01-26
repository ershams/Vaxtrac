from flask import Flask
app=Flask(__name__,template_folder='template')
import psycopg2
import requests
from pprint import pformat

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from model import connect_to_db, db, CompletedIMZ, User, Eligibility
import crud
import cloudinary.uploader
import os

os.system('source secrets.sh')

# CLOUDINARY_KEY = os.environ['CLOUDINARY_KEY']
# CLOUDINARY_SECRET = os.environ['CLOUDINARY_SECRET']
# CLOUD_NAME = "dg9svgk9f"

from jinja2 import StrictUndefined

app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def homepage():
    """View homepage."""

    return render_template("homepage.html")

@app.route("/sign-up")
def show_sign_up_form():
    """take use to sign-up form"""
    return render_template("registration.html")

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
        
        print(user)
        print(user.completedimzs)

    vaccine = crud.get_user_vaccine()
    date = crud.get_user_vaccine_date()
    reaction = crud.get_user_vaccine_reaction()
        
    return render_template("dashboard.html", vaccine=vaccine, date=date, reaction= reaction)

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

# @app.route("/post-form-data", methods=["POST"])
# def upload_image():
#     my_file = request.files['my-file']

#     result = cloudinary.uploader.upload(my_file,
#                                         api_key = CLOUDINARY_KEY,
#                                         api_secret = CLOUDINARY_SECRET,
#                                         cloud_name = CLOUD_NAME)

#     img_url = result['secure_url']
#     return redirect ('/dashboard', img_url=img_url)    

@app.route("/quiz")
def show_quiz():
    """take use to sign-up form"""

    return render_template("quiz.html")

# @app.route("/recommended", methods = "POST")
# def show_recommended():

#     gender = request.form.get('genderField')
#     age = request.form.get('dobField')
#     pregnant = request.form.get('pregnantField')
#     travel = request.form.get('travelField')
#     chickenpox = request.form.get('cpField')
#     fluids = request.form.get('bloodField')
#     injectables = request.form.get('injectField')

#     return render_template("recommended.html")

@app.route("/eligible_imz", methods=["POST"])
def find_eligible_imz():
    """log a new imz."""

    genderM = request.form.get('maleField')
    genderF = request.form.get('femaleField')
    genderN = request.form.get('nbField')
    age = request.form.get('dobField')
    pregnantY = request.form.get('pregnantYField')
    pregnantN = request.form.get('pregnantNField')
    travelY = request.form.get('travelYField')
    travelN = request.form.get('travelNField')
    chickenpoxY = request.form.get('cpYField')
    chickenpoxN = request.form.get('cpNField')
    chickenpoxU = request.form.get('cpUField')
    fluidsY = request.form.get('bloodYField')
    fluidsN = request.form.get('bloodNField')
    injectablesY = request.form.get('injectYField')
    injectablesN = request.form.get('injectNField')

    eligibility = crud.create_eligibility(genderM, genderF, genderN, age, pregnantY, pregnantN, 
                                        travelY, travelN, chickenpoxY, chickenpoxN, chickenpoxU, 
                                        fluidsY, fluidsN, injectablesY, injectablesN)

    db.session.add(eligibility)
    db.session.commit()

    

    return redirect("/recommended")

@app.route("/add_vaccines")
def show_vaccines():

    return render_template ('/add_vaccines.html')

@app.route('/allvaccines/search', methods = ['POST'])
def find_vaccines():
    """Search for vaccines"""

    brand_name = request.form.get('brand_name')

    
    url = 'https://api.fda.gov/drug/ndc.json'
    #pass in all search endpoints 
    payload = {'search': brand_name}


    response = requests.get(url, params=payload)
    data = response.json()
  
    genericName = data['results'][0]["generic_name"]
    print(genericName)
    
    if '_embedded' in data:
        vaccines = data['_embedded']['vaccines']
    else:
        vaccines = []

    return render_template('search-results.html',
                           pformat=pformat,
                           data=data,
                           results=vaccines)

@app.route("/recommended")
def show_results():

    # age = session.get('age')

    age = db.session.query(Eligibility.age).order_by(Eligibility.quiz_id.desc()).first()
    sex = db.session.query(Eligibility.gender).order_by(Eligibility.quiz_id.desc()).first()
    pregnant = db.session.query(Eligibility.pregnant).order_by(Eligibility.quiz_id.desc()).first()
    travel = db.session.query(Eligibility.travel).order_by(Eligibility.quiz_id.desc()).first()

    return render_template("recommended.html", age = age, sex=sex, pregnant=pregnant, travel=travel)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
