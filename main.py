from flask import Flask, render_template, session, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5444/maryjonesng'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key=b'\xcc\x839\xfcV\xf6\x96\xb3\xa9\x8a[\x94\x00\xeaN`v\xc9m\xe0\\L,\x0b'
db = SQLAlchemy(app)

import models

from admin import admin_page
app.register_blueprint(admin_page)


@app.route("/")
def index():
    return render_template('home.html', title="Mary Jones Nigeria Ltd", informatiion="Welcome")


@app.route("/products")
def products():
    produce = models.ProduceOluwatomilolaAdeniran.query.all()
    css = request.args.get('css', 'normal')
    return render_template('products-and-services.html', title="Products", information="View Products",
                           css=css,produce=produce)
    # return render_template('products-and-services.html', title="Products", information="View Products")


@app.route("/about-us")
def aboutus():
    return render_template('about-us.html', title="About Us", information="About Us")


@app.route("/signup/")
def signup():
    return render_template('signup.html', title="SIGN UP", information="Create an account!")


@app.route("/process-signup/", methods=['POST'])
def process_signup():     # Let's get the request object and extract the parameters sent into local variables.
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    othernames = request.form['othernames']
    email = request.form['email']
    password = request.form['password']
    try:
        user = models.UserOluwatomilolaAdeniran(firstname=firstname, lastname=lastname, othernames=othernames, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        information = 'Could not submit. The error message is {}'.format(e.__cause__)
        return render_template('signup.html', title="SIGN-UP", information=information)

    # If we have gotten to this point, it means that database write has been successful. Let us compose success info
    information = 'User by name {}  {} successfully added. The login name is the email address {}.'.format(firstname, lastname, email)
    return render_template('signup.html', title="SIGN-UP", information=information)


@app.route("/login/")
def login():
    session['next_url'] = request.args.get('next', '/')
    return render_template('login.html',  title="SIGN  IN",  information="Enter login details")


@app.route("/process-login/", methods=['POST'])
def process_login():
    email = request.form['email']
    password = request.form['password']
    if (authenticateUser(email, password)):
        session['username'] = email
        session['userroles'] = 'admin'
        return redirect(session['next_url'])
    else:
        error = 'Invalid user or password'
    return render_template('login.html', title="SIGN IN", information=error)


def authenticateUser(email, password):
    user = models.UserOluwatomilolaAdeniran.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return True
    else:
        return False


@app.route("/logout/")
def logout():
    session.pop('username', None)
    session.pop('userroles', None)
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(error):
 return render_template('page-not-found.html'), 404


if __name__ == "__main__":
    app.run(port=5021)
