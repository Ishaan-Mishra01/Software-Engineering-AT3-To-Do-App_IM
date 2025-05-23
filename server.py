from flask import Flask, render_template, redirect, url_for, request, flash
import secrets
from databases import User
import hashlib

app = Flask(__name__)
app.secret_key= secrets.token_hex(32) #32 byte secret key. used for verification between different pages
#app.config['SECRET_KEY'] = '12345'



@app.route('/', methods=['GET', 'POST'])
def home():
	return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode('utf-8')).hexdigest()
        
        new_user = User(username=username, email=email, password=password)
        User.db.session.add(new_user)

        error_msg = ""
        if len(email) <= 4 or len(email) >= 200: #Annoying probably will break cause it was causing errors before
            error_msg = "Email must be between 4 and 20 characters"
        elif len(username) <= 2 or len(email) >= 200: #Annoying probably will break cause it was causing errors before
              
            error_msg = "Username must be between 5 and _ characters"
        elif len(password) <= 8 or len(email) >= 200: #Annoying probably will break cause it was causing errors before
            error_msg = "Username must be between 8 and _ characters"
        
        if error_msg =="":
            return render_template("home.html")
        else:
            flash("error_msg", "danger")
            return redirect(url_for('login'))
        
    else:
        return render_template("login.html")
	    


if __name__ == '__main__':
	app.run()