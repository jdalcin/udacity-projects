from python.webpage_backend.webpage_handler import *

class RegistrationHandler(Handler):
	"""Webpage which allows a new user to register or an existing user to login into their blog."""

	def get(self):
		self.render('registration.html')

	def post(self):
		# 'registration.html' Form Information
		username_login = self.request.get('username-login').lower()
		password_login = self.request.get('password-login')
		username_registration = self.request.get('username-registration').lower()
		password_registration = self.request.get('password-registration')
		password_check_registration = self.request.get('verify-password-registration')
		#Login
		error_login = ''
		if self.request.get('login'):
			error_login = self.click_login(username_login, password_login, error_login)
		# New Registration
		error_registration = ''
		if self.request.get('registration'):
			error_registration = self.click_registration(username_registration, password_registration, 
				                                                       password_check_registration, error_registration)
		# Render Registration Page
		if error_login == '' or error_registration == '':
			self.render('registration.html', username_login = username_login, password_login = password_login, 
				        error_login = error_login, username_registration = username_registration, 
				        password_registration = password_registration, 
				        password_check_registration = password_check_registration, error_registration = error_registration)

	def click_login(self, username_login, password_login, error_login):
		"""Checks if login information submitted is valid. If information is valid, user is logged in. If not, an error pops up."""

		if username_login and password_login and User.get_by_key_name(username_login):
			hashed_password = User.get_by_key_name(username_login).password
			#checks if password inputted is valid	
			if hash.validate_login(username_login, password_login, hashed_password):
				self.response.headers.add_header('Set-Cookie', 
					                                             'username={}'.format(hash.make_cookie_secure(username_login)))
				self.redirect('/welcome')
			else:
				error_login = "Invalid password"
		elif username_login or password_login:
			error_login = "Invalid login"
		return error_login

	def click_registration(self, username_registration, password_registration, password_check_registration, error_registration):
		"""Checks if new user information is valid. If valid, user is logged in. If not, an error pops up."""

		# checks if user registered already exists and if registration form is properly filled
		if username_registration and User.get_by_key_name(username_registration):
			error_registration = "This user already exists"
		elif username_registration and password_registration and password_check_registration:
			if password_registration == password_check_registration:
				# hashes user's password
				hashed_password = hash.make_password_hash(username_registration, password_registration) 
				# adds user to the database
				User(key_name = username_registration, user = username_registration, password = hashed_password).put()
				self.response.headers.add_header('Set-Cookie', 
					                                             'username={}'.format(hash.make_cookie_secure(username_registration)))
				self.redirect('/welcome')
			else:
				error_registration = "Passwords do not match"
		elif username_registration or password_registration or password_check_registration:
			error_registration = "Invalid Registration"
		return error_registration

		
