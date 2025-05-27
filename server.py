from flask import Flask, render_template, redirect, url_for, request, flash
import secrets
from databases import db, User
import hashlib

app = Flask(__name__)
app.secret_key= secrets.token_hex(32) #32 byte secret key. used for verification between different pages
#app.config['SECRET_KEY'] = '12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:/site.db' #rename later
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False IDK 
db.init_app(app)

with app.app_context(): #creating tables which runs once app has started
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def home():
	return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode('utf-8')).hexdigest()

        error_msg = ""
        if len(email) <= 4 or len(email) >= 200: #Annoying probably will break cause it was causing errors before
            error_msg = "Email must be between 4 and 200 characters"
        elif len(username) <= 2 or len(email) >= 200: #Annoying probably will break cause it was causing errors before
              
            error_msg = "Username must be between 5 and 200 characters"
        elif len(password) <= 8 or len(email) >= 200: #Annoying probably will break cause it was causing errors before
            error_msg = "Username must be between 8 and 200 characters"
        
        if error_msg == "":
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('home'))
        else:
            flash(error_msg, "danger")
            return redirect(url_for('register'))

    return render_template("register.html")
	    


if __name__ == '__main__':
	app.run()