from flask import Flask
app=Flask(__name__,template_folder='template')
import psycopg2

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db, InfantVaccine, User
import crud

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
    name = request.form.get("name")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
            flash("The email or password you entered was incorrect.")
    else:
            # Log in user by storing the user's email in session
            session["user_email"] = user.email
            flash(f"Welcome back, {user.email}!")

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
        

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM completedimz where user is not null')
        vaccine = cur.fetchall()
        cur.close()
        conn.close()

        return render_template("dashboard.html", vaccine=vaccine)
    return redirect ('/')

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

# @app.route("/registration", methods=["POST"])
# def create_new_user():
#     """Create a new user."""

#     email = request.form.get("email")
#     password = request.form.get("password")
#     # fname = request.form.get("fname")
#     # lname = request.form.get("lname")

#     user = User.get_by_email(email)

#     if user:
#         flash("A user is already registered with that email.")
#     else:
#         user = User.create(email = email,
#                             password = password)
#         #                     fname = fname,
#         #                     lname=lname)
#         db.session.add(user)
#         db.session.commit()
#         flash(f"Welcome to MedBuddy! Please log in.")
    
#     return redirect("/")

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

# @app.route("/create_profile", methods=["POST"])
# def add_profile():
#     """Create and log a new profile."""
#     logged_in_email = session.get("user_email")
#     if logged_in_email:

#         user = crud.get_user_by_email(logged_in_email)

#         # print(user)

#         name = request.form.get('nameField')
#         # print(type(name))
#         age = request.form.get('dobField')
#         gender = request.form.get('gender')
        
#         profile = crud.create_profile(user, name, age, gender)
#         db.session.add(profile)
#         db.session.commit()

#     return redirect("/dashboard")

@app.route("/add-vaccine", methods=["POST"])
def process_add_vaccine():
    """Process user login."""

    # if request.method == 'POST':
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
            flash("The email or password you entered was incorrect.")
    else:
            # Log in user by storing the user's email in session
            session["user_email"] = user.email
            flash(f"Welcome back, {user.email}!")

    return redirect("/dashboard")

@app.route("/create_completed_imz", methods=["POST"])
def add_completed_imz():
    """log a new imz."""

    # user = crud.get_user_by_id(user_id)
    # logged_in_email = session.get(user_id)

    # user_id = User.query.get(user_id)

    imz = request.form.get('imzField')
    admin_date = request.form.get('adminDateField')
    reaction = request.form.get('reactionField')

    completed_imz = crud.create_completed_imz(imz, admin_date, reaction)

    db.session.add(completed_imz)
    db.session.commit()

    return redirect("/dashboard")

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

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
