import os
import random
import string
import httplib2
import json
import requests
import python.security.hash as encrypt

from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, make_response
from flask import session as login_session

from werkzeug import secure_filename

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

from sqlalchemy import create_engine, desc, exists, func
from sqlalchemy.orm import sessionmaker

from setup_database import Base, User, Item

# Create web application session
app = Flask(__name__)
app.config['upload_folder'] = 'static/images/uploads'

# Global Variables
category_list = ['Videogames', 'Books', 'Movies', 'Music', 'Technology', 'Food', 'Furniture']
file_extensions = ['png', 'jpg', 'jpeg', 'gif']

# Create database session
engine = create_engine('sqlite:///item_catalog.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine
database_session = sessionmaker(bind = engine)
session = database_session()

# returns the value of a dictionary
# if no value, returns an empty string rather than None
def return_value(dictionary):
	def result(key):
		if dictionary is None:
			return ''
		else:
			return dictionary.get(key)
	return result

def create_state_token():
	return ''.join(random.choice(string.ascii_uppercase + string.digits) for character in xrange(50))

def get_user_id(name = None, email = None):
	if not name and not email:
		return None
	elif not email: # for login case where email is not given but username is
		email = session.query(User.email).filter(func.lower(User.name) == name.lower()).scalar()
	if email:
		user_id = session.query(User.id).filter(func.lower(User.email) == email.lower()).scalar()
		return user_id
	else:
		return None

# creates users. User made through a third-party will be given an encrypted_password.
def create_user(login_details, encrypted_password = encrypt.make_password_hash("WUBBA", "LUBBA") ):
	session.add(User(name = login_details['username'], email = login_details['email'], encrypted_password = encrypted_password))
	session.commit()
	login_session['user-id'] = get_user_id(email = login_details['email'])
	user_picture = upload_file(login_details.get('picture'), login_session['user-id'], 'users' )
	if user_picture:
		login_session['picture'] = user_picture
		user = session.query(User).filter(User.id == login_session['user-id']).first()
		user.picture = user_picture
		session.commit()

def update_user_session_credentials(user_id):
	login_session['email'] = session.query(User.email).filter(User.id == user_id).scalar()
	login_session['picture'] = session.query(User.picture).filter(User.id == user_id).scalar()
	login_session['username'] = session.query(User.name).filter(User.id == user_id).scalar()

# checks if given file string is allowed
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in file_extensions

# takes in a flask File object, int file_id, and subfolder which represents  a string of subfolder of File lies in
# returns the string url for an uploaded file.
# each file is specific to its item. 
def upload_file(file, file_id, subfolder):
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		filename = str(file_id) + '-' + filename
		path_to_directory = os.path.join(app.config['upload_folder'], subfolder)
		if not os.path.exists(path_to_directory):
			os.makedirs(path_to_directory)
		path_to_file = os.path.join(path_to_directory, filename)
		file.save(path_to_file)
		return path_to_file
	else:
		return None

# deletes filename from operating system
def delete_file(filename):
	if filename and os.path.exists(filename):
		os.remove(filename)


# Creates registration screen
@app.route('/registration', methods = ['GET', 'POST'])
def registration_screen():
	if request.method == 'GET':
		state = create_state_token()
		login_session['state'] = state
		return render_template('registration.html', registration_details = return_value(None), state = state)
	elif request.method == 'POST':
		registration_details = request.form
		name_lowercase = registration_details['username'].lower()
		email_lowercase = registration_details['email'].lower()
		error = ''
		# makes sure request is from site and not an external malicous website
		if request.form.get('state') != login_session['state']:
			response = make_response(json.dumps('Invalid State Parameter'), 401)
			response.headers['Content-Type'] = 'application/json'
			return response
		# checks if supplied username and email is already in the database
		if not session.query(exists().where(func.lower(User.name) == name_lowercase)).scalar():
			if not registration_details.get('email') or not session.query(exists().where(func.lower(User.email) == email_lowercase)).scalar():
				if registration_details['password'] == registration_details['verify-password']:
					login_session['username'] = registration_details['username']
					login_session['email'] = registration_details['email']
					login_session['picture'] = request.files.get('picture')
					create_user(login_session, encrypted_password = encrypt.make_password_hash(name_lowercase, registration_details['password']))
					return redirect(url_for('homepage'))
				else:
					error = "Passwords must match"
			else:
				error = "Email already taken"
		else:
			error = "Name already taken"
		return render_template('registration.html', registration_details = return_value(registration_details), state = request.form.get('state'), error = error)

# Creates login screen
@app.route('/login', methods = ['GET'])
def login_screen():
	if request.method == 'GET':
		# Create cross-site request forgery token
		state = create_state_token()
		login_session['state'] = state
		return render_template('login.html', state = state)
	

@app.route('/login/submit', methods = ['POST'])
def first_party_login():
	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')
		error = ''
		if request.form.get('state') != login_session['state']:
			response = make_response(json.dumps('Invalid State Parameter'), 401)
			response.headers['Content-Type'] = 'application/json'
			return response
		if session.query(exists().where(func.lower(User.name) == username.lower())).scalar():
			encrypted_password = session.query(User.encrypted_password).filter(func.lower(User.name) == username.lower()).scalar()
			if encrypt.validate_login(username, password, encrypted_password):
				login_session['user-id'] = get_user_id(name = username)
				update_user_session_credentials(login_session['user-id'])
				return redirect(url_for('homepage'))
			else:
				error = "Invalid password"
		else:
			error = "Invalid username"
		return render_template('login.html', username = username, password = password, state = request.form['state'], error = error)

@app.route('/login/google-login', methods = ['POST'])
def google_login():
	if request.method == 'POST':
		print("processing")
		if request.args.get('state') != login_session['state']:
			response = make_response(json.dumps('Invalid State Parameter'), 401)
			response.headers['Content-Type'] = 'application/json'
			return response
		code = request.data
		CLIENT_ID = json.loads(open('google_client_secrets.json', 'r').read())['web']['client_id']
		oauth_flow = flow_from_clientsecrets('google_client_secrets.json', scope='')
		oauth_flow.redirect_uri = 'postmessage'
		credentials = oauth_flow.step2_exchange(code)

		# Check that the access token is valid.
		access_token = credentials.access_token
		url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
		       % access_token)
		h = httplib2.Http()
		result = json.loads(h.request(url, 'GET')[1])

		# If there was an error in the access token info, abort.
		if result.get('error') is not None:
			response = make_response(json.dumps(result.get('error')), 500)
			response.headers['Content-Type'] = 'application/json'
			return response

		# Verify that the access token is used for the intended user.
		gplus_id = credentials.id_token['sub']
		if result['user_id'] != gplus_id:
			response = make_response(json.dumps("Token's user ID doesn't match given user ID."), 401)
			response.headers['Content-Type'] = 'application/json'
			return response

		# Verify that the access token is valid for this app.
		if result['issued_to'] != CLIENT_ID:
			response = make_response(json.dumps("Token's client ID does not match app's."), 401)
			response.headers['Content-Type'] = 'application/json'
			return response

		stored_credentials = login_session.get('credentials')
		stored_gplus_id = login_session.get('gplus_id')

		# Store the access token in the session for later use.
		login_session['credentials'] = credentials
		login_session['gplus_id'] = gplus_id

		# Get user info
		userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
		params = {'access_token': credentials.access_token, 'alt': 'json'}
		answer = requests.get(userinfo_url, params=params)

		data = answer.json()

		login_session['username'] = data['name']
		login_session['picture'] = data['picture']
		login_session['email'] = data['email']
		print('update data')
		print login_session['username']
		# See if a user exists, if it doesn't make a new one
		user_id = get_user_id(email = login_session['email'])
		if not user_id:
			if not session.query(User.id).filter(func.lower(User.name) == login_session['username'].lower()).scalar(): # if name has not been taken
				create_user(login_session)
			else:
				return 'username_taken'
		else: # if user exists checks if user has a pre-existing account. If so, uses that username instead of making new one.
			prev_username = session.query(User.name).filter(User.id == user_id).scalar()
			if prev_username:
				login_session['username'] = prev_username
			user = session.query(User).filter(User.id == user_id).scalar()
			user.picture = login_session.get('picture')
			session.commit()
		login_session['user-id'] = get_user_id(email = login_session['email'])
		return 'logged_in'

@app.route('/login/facebook-login', methods = ['POST'])
def facebook_login():
	if request.method == 'POST':
		if request.args.get('state') != login_session['state']:
			response = make_response(json.dumps('Invalid State Parameter'), 401)
			response.headers['Content-Type'] = 'application/json'
			return response
		access_token = request.data

		app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
		    'web']['app_id']
		app_secret = json.loads(
		    open('fb_client_secrets.json', 'r').read())['web']['app_secret']

		url = ('https://graph.facebook.com/v2.8/oauth/access_token?'
		       'grant_type=fb_exchange_token&client_id=%s&client_secret=%s'
		       '&fb_exchange_token=%s') % (app_id, app_secret, access_token)

		h = httplib2.Http()
		result = h.request(url, 'GET')[1]
		data = json.loads(result)
		token = 'access_token=' + data['access_token']

		# Use token to get user info from API
		userinfo_url = "https://graph.facebook.com/v2.8/me/"

		url = 'https://graph.facebook.com/v2.8/me?%s&fields=name,id,email' % token
		h = httplib2.Http()
		result = h.request(url, 'GET')[1]
		data = json.loads(result)

		login_session['provider'] = 'facebook'
		login_session['username'] = data["name"]
		login_session['email'] = data["email"]
		login_session['facebook_id'] = data["id"]

		stored_token = token.split("=")[1]
		login_session['access_token'] = stored_token

		# Get user picture
		url = 'https://graph.facebook.com/v2.8/me/picture?%s&redirect=0&height=200&width=200' % token
		h = httplib2.Http()
		result = h.request(url, 'GET')[1]
		data = json.loads(result)

		login_session['picture'] = data["data"]["url"]

		# see if user exists
		user_id = get_user_id(email = login_session['email'])
		if not user_id: # if user does not exist
			if not session.query(User.id).filter(func.lower(User.name) == login_session['username'].lower()).scalar(): # if name has not been taken
				create_user(login_session) # then create user
				user_id = get_user_id(email = login_session['email'])
			else:
				return 'username_taken'
		else: # if user exists checks if user has a pre-existing account. If so, uses that username instead of making a new one.
			prev_username = session.query(User.name).filter(User.id == user_id).scalar()
			if prev_username:
				login_session['username'] = prev_username
			user = session.query(User).filter(User.id == user_id).scalar()
			user.picture = login_session.get('picture')
			session.commit()

		login_session['user-id'] = user_id
		return 'logged_in'

# Methods to end server-side access-token usage from third-party websites
def fbdisconnect():
	facebook_id = login_session['facebook_id']
	access_token = login_session['access_token']
	url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
	h = httplib2.Http()
	result = h.request(url, 'DELETE')[1]

def gdisconnect():
	credentials = login_session.get('credentials')
	access_token = credentials.access_token
	url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
	h = httplib2.Http()
	result = h.request(url, 'GET')[0]

# Creates general logout
@app.route('/logout', methods = ['POST'])
def logout():
	if request.method == 'POST':
		# checks if session is logged in by google or facebook
		if login_session.get('credentials'):
			gdisconnect()
		elif login_session.get('facebook_id'):
			fbdisconnect()
		login_session.clear() # clears session data regardless of login
		return redirect(url_for('homepage'))


# Creates homepage
@app.route('/')
def homepage():
	if request.method == 'GET':
		item_list = session.query(Item.name, Item.category, Item.id).order_by(desc(Item.date_uploaded)).limit(10).all()
		return render_template('homepage.html', login_session = login_session, item_list = item_list, category_list = category_list)

# Creates category page
@app.route('/category/<category_name>')
def category_page(category_name):
	if request.method == 'GET':
		item_list = session.query(Item.name, Item.id).filter(Item.category == category_name).all()
		if not category_name in category_list:
			response = make_response(json.dumps("Invalid URL"), 401)
			response.headers['Content-Type'] = 'application/json'
			return response
		return render_template('category.html', login_session = login_session, item_list = item_list, category_list = category_list, category_name = category_name)

@app.route('/<item_id>', methods = ['GET', 'POST'])
def item_page(item_id):
	if request.method == 'GET':
		item = session.query(Item).filter(Item.id == item_id).first()
		if not item:
			response = make_response(json.dumps("Invalid URL"), 401)
			response.headers['Content-Type'] = 'application/json'
			return response
		owner = session.query(User).filter(User.id == item.user_id).scalar()
		return render_template('item-info.html', owner = owner, item = item, category_list = category_list, login_session = login_session)

@app.route('/<item_id>/delete', methods = ['POST'])
def delete(item_id):
	if request.form.get('state') != login_session.get('state'):
		response = make_response(json.dumps('Invalid State Parameter'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	item = session.query(Item).filter(Item.id == item_id).scalar()
	if not item:
		response = make_response(json.dumps("Invalid URL"), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	if item.user_id != login_session['user-id']:
		response = make_response(json.dumps("Cannot Delete Other User's Content"), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	delete_file(item.picture)
	session.delete(item)
	session.commit()
	return redirect(url_for('homepage'))

@app.route('/<item_id>/edit', methods = ['GET', 'POST'])
def edit(item_id):
	item = session.query(Item).filter(Item.id == item_id).first()
	if not item:
		response = make_response(json.dumps("Invalid URL"), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	if item.user_id != login_session['user-id']:
		response = make_response(json.dumps("Cannot Edit Other User's Items "), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	if request.method == 'GET':
		return render_template('item-edit.html', item = item, category_list = category_list, login_session = login_session)
	elif request.method == 'POST':
		if request.form.get('state') != login_session.get('state'):
			response = make_response(json.dumps('Invalid State Parameter'), 401)
			response.headers['Content-Type'] = 'application/json'
			return response
		item_name = request.form.get('item-name')
		item_category = request.form.get('item-category')
		item_description = request.form.get('item-description')
		item_filename = upload_file(request.files.get('item-picture'), item_id, 'items')
		if item_filename:
			delete_file(str(item.picture))
		item.picture = item_filename
		item.name = item_name
		item.category = item_category
		item.description = item_description
		session.commit()
		return redirect('/' + str(item_id))

@app.route('/item/add', methods = ['GET', 'POST'])
def add_item():
	if request.method == 'GET':
		return render_template('item-add.html', category_list = category_list, login_session = login_session)
	if request.method == 'POST':
		if request.form.get('state') != login_session.get('state'):
			response = make_response(json.dumps('Invalid State Parameter'), 401)
			response.headers['Content-Type'] = 'application/json'
			return response
		item_name = request.form.get('item-name')
		item_category = request.form.get('item-category')
		item_description = request.form.get('item-description')
		new_item = Item(name = item_name, category = item_category, description = item_description, user_id = login_session['user-id'])
		session.add(new_item)
		session.flush()
		item_id = new_item.id
		filename = upload_file(request.files.get('item-picture'), item_id, 'items')
		if filename:
			new_item.picture = filename
		session.commit()
		return redirect('/' + str(item_id))

# JSON API's to view item information
@app.route('/JSON')
def latest_items_JSON():
	if request.method == 'GET':
		latest_items = session.query(Item).order_by(desc(Item.date_uploaded)).limit(10).all()
		item_array = []
		for item in latest_items:
			item_owner = session.query(User.name).filter(User.id == item.user_id).scalar()
			item.item_owner_name = item_owner
			item_array.append(item.serialize)
		return jsonify(latest_items = item_array)

@app.route('/category/<category_name>/JSON')
def category_items(category_name):
	if request.method == 'GET':
		if not category_name in category_list:
			response = make_response(json.dumps("Invalid URL"), 401)
			response.headers['Content-Type'] = 'application/json'
			return response
		category_items = session.query(Item).filter(Item.category == category_name).all()
		item_array = []
		for item in category_items:
			item_owner = session.query(User.name).filter(User.id == item.user_id).scalar()
			item.item_owner_name = item_owner
			item_array.append(item.serialize)
		return jsonify(category_items = item_array)

@app.route('/<item_id>/JSON')
def item_info(item_id):
	if request.method == 'GET':
		item = session.query(Item).filter(Item.id == item_id).first()
		if not item:
			response = make_response(json.dumps("Invalid URL"), 401)
			response.headers['Content-Type'] = 'application/json'
			return response
		item_owner = session.query(User.name).filter(User.id == item.user_id).scalar()
		item.item_owner_name = item_owner
		return jsonify(item_info = item.serialize)

if __name__ == '__main__':
	port = 8080
	host = '0.0.0.0'
	app.debug = True
	app.secret_key = '3d41ea24cd403b023df2524573ac03f09bad16f653162c50'
	print "Running in port " + str(port)
	app.run(host=host, port = port)