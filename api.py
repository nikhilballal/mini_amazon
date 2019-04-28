from flask import Flask,render_template,request,redirect,session, url_for,flash
from model import check_user, create_user,log_user,check_product,create_product,get_products,seller_products,cart_page,update_cart,remove_from_cart
app = Flask(__name__) # we are including all the properties of Flask into the app
app.config['SECRET_KEY']='hello' #for session to work, we need secret_key

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route("/login", methods = ["GET","POST"]) #if 'get' is not mentioned won't allow page to go back to 'home'
def login():
    if request.method == 'POST': # "POST" - typing it out on a form. "GET" clicking a link on the page or putting link on address bar.
        uname = request.form['username']
        password = request.form['password']
        result = log_user(uname) #result will store the username entered however will contain the info i.e username, password, custtype and email of the entry used in 'log_user'

        if password == result['password']:
            session['username'] = result['username']
            session['c_type'] = result['c_type']
            return redirect(url_for('welcome'))
        flash ("enter correct password")
        return redirect(url_for('home'))

    return redirect(url_for('home')) # if not POST, return to home page.

@app.route("/signup", methods = ['GET','POST'])
def signup():
    if request.method == 'POST':

        user_info= {} #creating a dictionary to pass the below code into database - users

        user_info['username'] = request.form['username']
        user_info['email'] = request.form['email']
        user_info['password'] = request.form['password']
        rpassword = request.form['rpassword']
        user_info['c_type'] = request.form['type']
        if user_info['c_type'] == "buyer":
            user_info['cart'] = []



        if check_user(user_info['username']) is False:
            if rpassword == user_info['password']:
                create_user(user_info) #we are passing the dictionary into the function 'create_user'
            else:
                flash("passwords do not match, please provide correct password")
                return render_template("register.html")
        else:
            return "user already exists"

    return render_template("register.html")

@app.route("/addproduct", methods=['GET','POST'])
def add_product():

    if request.method == 'POST':

        product_info={}

        product_info['productsname'] = request.form['productsname']
        product_info['description'] = request.form['description']
        product_info['cost'] = int(request.form['cost']) # storing the cost as int in key of dictionary
        product_info['seller_name'] = session['username']

        if check_product(product_info['productsname']) is False:
            create_product(product_info) #this you will find in model.py
            return "your product has been added"
        else:
            return "type another product"

    return redirect(url_for('welcome'))

@app.route("/productslist")
def getprod():
    products = get_products()
    return render_template("products.html", products = products)

@app.route("/sellerproducts")
def yourproduct():
    prods = seller_products(session["username"])
    return render_template("products.html" , prods = prods)

@app.route('/add_cart', methods = ['POST'])
def add_cart():
    product_id = request.form['product_id']
    update_cart(session["username"], product_id)
    return redirect(url_for('cart'))

@app.route('/cart')

def cart():
    products = cart_page(session['username'])
    return render_template("cart_page.html", products=products)

@app.route('/remove_cart', methods = ['POST'])
def remove_cart():
    product_id = str(request.form['product_id'])
    remove_from_cart(session['username'],product_id)
    return redirect(url_for('cart'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if(__name__) == '__main__':
    app.run(debug= "True")
