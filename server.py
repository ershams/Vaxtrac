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
    print(user.name)
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

    if "user_id" in session:

        user_id = session["user_id"] 

        name = crud.get_user_by_id(user_id).name

        vaccine = crud.get_user_by_id(user_id).completedimzs

        return render_template("dashboard.html", vaccine=vaccine, name=name)

@app.route("/create_completed_imz", methods=["POST"])
def add_completed_imz():
    """log a new imz."""

    if 'user_id' not in session:
        return redirect("/")

    user_id = session.get('user_id')

    imz = request.form.get('imzField')
    admin_date = request.form.get('adminDateField')
    reaction = request.form.get('reactionField')

    if imz: 
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
    """take user to eligibility quiz"""

    return render_template("quiz.html")

@app.route("/retake_quiz", methods = ["POST"])
def retake_quiz():
    """take use to sign-up form"""

    return redirect("/quiz")


@app.route("/eligible_imz", methods=["POST"])
def find_eligible_imz():
    """log a new imz."""

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

    check_age = crud.calculate_age(age)
    vaccine = crud.get_recommended_vaccines(check_age)

    return  render_template("recommended.html", 
                            pregnantY=pregnantY, travelY=travelY, 
                            vaccine=vaccine, check_age=check_age,
                            injectablesY=injectablesY, chickenpoxY=chickenpoxY,
                            chickenpoxU=chickenpoxU)

@app.route("/add_vaccines")
def show_vaccines():

    return render_template ('/add_vaccines.html')

@app.route('/allvaccines/search', methods = ['POST'])
def find_vaccines():
    """Search for vaccines"""

    json = request.get_json()
    brand_name = None

    if json:
        brand_name = json["brand_name"]

    # request.
    url = 'https://api.fda.gov/drug/ndc.json'
    #pass in all search endpoints 
    payload = {'search': brand_name}


    response = requests.get(url, params=payload).json()
    # print(data)
    query = response['results'][0]['brand_name']
    data = crud.get_pt_education(query)
    
    if data :
        return {
            "status": " ",
            "uses": data['uses'],
            "warnings": data['warning']}

    return {"status": "Not Found",
            "brand_name": brand_name}

@app.route('/findprovider', methods = ['POST'])
def find_provider():
    """Search for vaccines"""

    json = request.get_json()
    loc_admin_zip = None
    print(json)

    if json:
        loc_admin_zip = json["loc_admin_zip"]

    # request.
    url = 'https://data.cdc.gov/resource/bugr-bbfr.json'
    #pass in all search endpoints 
    payload = {'loc_admin_zip': loc_admin_zip}

    # print(payload)

    response = requests.get(url, params=payload).json()
    name = response[0]['loc_name']
    address = response[0]['loc_admin_street1']
    city = response[0]['loc_admin_city']
    phone = response[0]['loc_phone']
    print(address)
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    

    return {"name" : name,
            "address" : address,
            "city" : city,
            "phone" : phone}

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True, port=3800)
