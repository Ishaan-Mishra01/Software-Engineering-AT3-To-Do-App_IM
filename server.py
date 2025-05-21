from flask import Flask, render_template, redirect, url_for, request, flash

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
	return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        
        error_msg = ""
        if len(email) <= 4:
                error_msg = "Email must be between 4 and 20 characters"
        elif len(username) <= 5:
              
                error_msg = "Username must be between 5 and _ characters"
        elif len(password) <= 8:
                error_msg = "Username must be between 5 and _ characters"
              #return must have and email\
        if error_msg =="":
               return render_template("home.html")
        else:
               flash(error_msg)
	    


if __name__ == '__main__':
	app.run()