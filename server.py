from flask import Flask
app=Flask(__name__,template_folder='template')

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
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
        print('!!!!')

        logged_in_email = session.get("user_email")
        user = crud.get_user_by_email(logged_in_email)

        return render_template("dashboard.html", profiles = user.profiles)
    return redirect ('/')

@app.route("/sign-up")
def show_sign_up_form():
    """take use to sign-up form"""
    return render_template("registration.html")

@app.route("/quiz")
def show_quiz():
    """take use to sign-up form"""
    return render_template("quiz.html")

@app.route("/registration", methods=["POST"])
def register_user():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")
    name = request.form.get("name").capitalize()

    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
        return redirect('/registration')
    else:
        user = crud.create_user(email, password, name)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return render_template('registration.html')

@app.route("/create_profile", methods=["POST"])
def add_profile():
    """Create and log a new profile."""
    logged_in_email = session.get("user_email")
    if logged_in_email:

        user = crud.get_user_by_email(logged_in_email)
        # user=user, name=name, age=age, vaccine_status=vaccine_status)

        name = request.form.get('nameField')
        print(type(name))
        age = request.form.get('dobField')
        # vaccine = request.form.get('vaccine')
        gender = request.form.getlist('gender')

        profile = crud.create_profile(user, name, age)
        db.session.add(profile)
        db.session.commit()

    return redirect("/dashboard")
    


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
