import random
import string
import httplib2
import json
import python.security.hash as encrypt

from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, make_response
from flask import session as login_session

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

from sqlalchemy import create_engine, desc, exists, func
from sqlalchemy.orm import sessionmaker

from setup_database import Base, User, Item

# Create web application session
app = Flask(__name__)


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
def create_user(login_session, encrypted_password = encrypt.make_password_hash("WUBBA", "LUBBA") ):
	session.add(User(name = login_session['username'], email = login_session['email'], picture = login_session['picture'], encrypted_password = encrypted_password))
	session.commit()


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
			return redirect(url_for('homepage'))
		# checks if supplied username and email is already in the database
		if not session.query(exists().where(func.lower(User.name) == name_lowercase)).scalar():
			if not registration_details.get('email') or not session.query(exists().where(func.lower(User.email) == email_lowercase)).scalar():
				if registration_details['password'] == registration_details['verify-password']:
					login_session['username'] = registration_details['username']
					login_session['email'] = registration_details['email']
					login_session['picture'] = registration_details['picture']
					create_user(login_session, encrypted_password = encrypt.make_password_hash(name_lowercase, registration_details['password']))
					login_session['user-id'] = get_user_id(email = registration_details['email'])
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
			return redirect(url_for('homepage'))
		if session.query(exists().where(User.name == username)).scalar():
			encrypted_password = session.query(User.encrypted_password).filter(func.lower(User.name) == username.lower()).one()[0]
			if encrypt.validate_login(username, password, encrypted_password):
				login_session['user-id'] = get_user_id(name = username)
				return redirect(url_for('homepage'))
			else:
				error = "Invalid password"
		else:
			error = "Invalid username"
		return render_template('login.html', username = username, password = password, state = state, error = error)

@app.route('/login/google-login', methods = ['POST'])
def google_login():
	if request.method == 'POST':
		return 'the way the world works'

@app.route('/login/facebook-login', methods = ['POST'])
def facebook_login():
	if request.method == 'POST':
		if request.args.get('state') != login_session['state']:
			return url_for('homepage')
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
		else:
			print("User exists")
		login_session['user-id'] = user_id

		output = ''
		output += '<h1>Welcome, '
		output += login_session['username']

		output += '!</h1>'
		output += '<img src="'
		output += login_session['picture']
		output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

		flash("Now logged in as %s" % login_session['username'])
		return output

# Creates homepage
@app.route('/')
def homepage():
	return "Username: " + login_session['username'] + "\nEmail: " + login_session['email'] + "\nPicture: " + login_session['picture'] + "         User-ID: " + str(login_session['user-id']) + "\nEncrypted_Password: " + session.query(User.encrypted_password).filter(User.email == login_session['email']).scalar()

if __name__ == '__main__':
	port = 8080
	host = '0.0.0.0'
	app.debug = True
	app.secret_key = '3d41ea24cd403b023df2524573ac03f09bad16f653162c50'
	print "Running in port " + str(port)
	app.run(host=host, port = port)