from flask import Flask, render_template, flash, redirect, url_for, session, logging, request, send_from_directory

from flask_mysqldb import MySQL, MySQLdb
from passlib.hash import sha256_crypt
import json
from forms import SignUpForm

app = Flask(__name__)

# make an instance of mysql
mysql = MySQL(app)

# open config file
with open('config.json') as config_file:
    config_data = json.load(config_file)

# database configuration
db_settings = config_data['database']
app.config.update(db_settings)


# home endpoint
@app.route("/", methods=['GET', 'POST'])
def home():

    return render_template("home.html")


# allbooks endpoint
@app.route("/all_books", methods=['GET', 'POST'])
def all_books():

    return render_template("allBooks.html")


# shortstories endpoint
@app.route("/short_stories", methods=['GET', 'POST'])
def short_stories():

    return render_template("shortstories.html")


# music endpoint
@app.route("/music", methods=['GET', 'POST'])
def music():

    return render_template("song.html")


# video endpoint
@app.route("/video", methods=['GET', 'POST'])
def video():

    return render_template("songVideo.html")


# poetry endpoint
@app.route("/poetry", methods=['GET', 'POST'])
def poetry():

    return render_template("poetry.html")


# admin endpoint
@app.route("/admin", methods=['GET', 'POST'])
def admin():

    return render_template("admin.html")


# book endpoint
@app.route("/book", methods=['GET', 'POST'])
def book():

    return render_template("book.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignUpForm(request.form)

    if request.method == 'POST' and form.validate():

        # get the remaining data
        name = form.name.data
        email = form.email.data
        password = sha256_crypt.hash(str(form.password.data))

        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users(name, email, password) \
                                    VALUES(%s, %s, %s)",
                        (name, email, password))

            # commit to database
            # cur.connection.commit()

            output = cur.fetchall()
            columns = output[0]
            id_ = columns['id']
            print(id_)

            # commit to db
            cur.connection.commit()

            cur.close()

        except (MySQLdb.Error, MySQLdb.Warning) as error:
            return render_template("login.html", error=error, form=form)

        # token = s.dumps(email, salt='email-confirmation-key')
        # msg = Message('confirmation', sender='olaseth39@gmail.com', recipients=[email])
        # link = url_for('confirm', token=token, eml=email, _external=True)
        # msg.body = "Welcome! Thanks for signing in. Please follow this link to activate your account " + link
        # mail.send(msg)

        flash("Signed up successfully", "success")

        return redirect(url_for("admin"))

        # return render_template("confirmation_msg.html", email=email)

    return render_template("login.html", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password_candidate = request.form['password']

        # create a cursor
        cur = mysql.connection.cursor()

        result = cur.execute("SELECT * FROM users WHERE email = %s ", [email])

        cur.connection.commit()

        # Check if the email has been used
        if result > 0:
            data = cur.fetchone()
            password = data['password']
            user_id = data['id']

            # compare passwords
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['email'] = email   # one email in session in the confirm route has been used
                session['user_id'] = user_id
                flash("You are Logged in successfully", "success")
                return redirect(url_for("admin"))
            else:
                error = "Invalid email or password"
                return render_template("login.html", error=error)

            # close connection
            cur.close()

        else:
            error = "Email or Password not found"
            return render_template("login.html", error=error)

        return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)