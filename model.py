from pymongo import MongoClient
client = MongoClient()
db = client["mini_amazon"]

def check_user(username):

    query = {"username": username}  #creating a dict to do a query into the database
    results = db['users'].find(query) # find returns pointer object

    if results.count()>0:
        return True
    return False

def create_user(user_info):
    db['users'].insert_one(user_info) #inserting the dictionary in the function to the database

def log_user(username):
    query = {"username": username} #query is returning the entire entry of dict from the database where this 'username:vishak' key-value pair exists in the database.
    results = db['users'].find_one(query) #find one instance of username in database, typing only 'find' only will return only cursor object.
    return results

def check_product(name):

    query = {"productsname": name}  #creating a dict to do a query into the database
    results = db['products'].find(query) # find returns pointer object

    if results.count()>0:
        return True
    return False

def create_product(x):
    db['products'].insert_one(x) #inserting the dictionary in the function to the database

def get_products():
    return db['products'].find({}) #find fetches the data

def seller_products(username):
    query = {"seller_name": username}
    results = db['products'].find(query)
    return results
