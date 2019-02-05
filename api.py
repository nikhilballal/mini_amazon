from flask import Flask,render_template, request,redirect,session, url_for
app = Flask(__name__) # we are including all the properties of Flask into the app
app.config['SECRET_KEY']='hello'

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/home")
def home():
    if session.get('username'):
        return render_template('home.html',user = session['username'])
    else:
        return render_template('home.html')

@app.route("/login", methods = ["GET","POST"]) #if 'get' is not mentioned wont allow page to go back to 'home'
def login():
    if request.method == 'POST':
        vishak = {'uname': 'vishak', 'password': '12345'}


        uname = request.form['username']
        password = request.form['password']

        if vishak['uname'] == uname and vishak['password'] == password:
            session['username'] = uname
            session['password'] = password


    #return render_template("home.html")
    return redirect(url_for('home')) # from def home()

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('home'))

if(__name__) == '__main__':
    app.run(debug="True")
