from pymongo import MongoClient
from flask import session

client= MongoClient()
db = client['amazon_valley']

def check_user(username):

	query ={'username':username}
	result =db['users'].find_one(query)
	return result

def add_user_to_db(user_info):
	
	db['users'].insert_one(user_info) 

def check_product(name):

	query={'name':name}
	result = db['products'].find_one(query)
	return result

def add_product_to_db(product_info):
	db['products'].insert_one(product_info)

def get_products():

	if session['c_type'] == 'buyer':

		result= db['products'].find({})
		return result

	query = {"seller":session['username']}
	result=db['products'].find(query)
	return result

def remove_product(product):

	db['products'].remove({"name":product})

def add_to_cart(name):

	query={"username":session['username']}
	action ={"$addToSet":{"cart":{"$each":[name]}}}

	db['users'].update(query,action)

def get_cart():

	query ={"username":session['username']}
	temp = db['users'].find_one(query)
	result = temp['cart']

	cart = []
	total=0

	for product in result:
		info = db['products'].find_one({"name":product})
		cart.append(info)
		total+=info['price']

	return cart,total

def remove_from_cart(name):

	query = {"username":session['username']}
	action = {"$pull":{"cart":name}}

	db['users'].update(query,action)