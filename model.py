from pymongo import MongoClient
from bson.objectid import ObjectId
client = MongoClient()
db = client["mini_amazon"]


def check_user(username):

    # creating a dict to do a query into the database
    query = {"username": username}
    results = db['users'].find(query)  # find returns pointer object

    if results.count() > 0:
        return True
    return False


def create_user(user_info):
    # inserting the dictionary in the function to the database
    db['users'].insert_one(user_info)


def log_user(username):
    # query is returning the entire entry of dict from the database where this 'username:vishak' key-value pair exists in the database.
    query = {"username": username}
    # find one instance of username in database, typing only 'find' will return data along with cursor object.
    results = db['users'].find_one(query)
    return results


def check_product(name):
    # query is to check what is passed as productsname in the db
    query = {"productsname": name}
    # return query and store the results pertaining to the query.
    results = db['products'].find(query)

    if results.count() > 0:
        return True
    return False


def create_product(x):
    # inserting the dictionary in the function to the database
    db['products'].insert_one(x)


def get_products():
    return db['products'].find({})  # find fetches the data


def seller_products(name):
    query = {"seller_name": name}
    results = db['products'].find(query)
    return results


def update_cart(username, product_id):  # when i press 'buy' the products.html.
    query = {"username": username}
    result = db['users'].find_one(query)
    if result['cart'].get(product_id):
        db["users"].update({"username": username}, {
                           "$inc": {"cart.{}".format(product_id): 1}})

    else:
        db["users"].update({"username": username}, {
                           "$set": {"cart.{}".format(product_id): 1}})


def cart_page(username):
    query = {"username": username}
    results = db["users"].find_one(query)
    product_ids = results.get('cart').keys()

    products = []
    for product_id in product_ids:
        query = {"_id": ObjectId(product_id)}
        results = db['products'].find_one(query)
        products.append(results)

    return products


def remove_from_cart(username, product_id):
    query = {'username': username}
    result = db['users'].find_one(query)

    if result['cart'].get(product_id) <= 1:
        db['users'].update({'username': username}, {"$unset": {f"cart.{product_id}": 1}})
        return True
    db['users'].update({'username': username}, {"$inc": {f"cart.{product_id}": -1}})
