from python.webpage_backend.webpage_handler import *

class RegistrationRegisterHandler(Handler):
	
	def post(self):
		username_registration = self.request.get('username-registration')
		password_registration = self.request.get('password-registration')
		password_check_registration = self.request.get('verify-password-registration')
		error_registration = self.click_registration(username_registration, password_registration, 
				                                            password_check_registration)
		if error_registration != '':
			self.render('registration.html', username_registration = username_registration, 
				        password_registration = password_registration, 
				        password_check_registration = password_check_registration, error_registration = error_registration)

	def click_registration(self, username_registration, password_registration, password_check_registration, error_registration = ''):
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
					                                             'username={};Path=/'.format(hash.make_secure(
					                                             	                                    username_registration.lower())))
				self.redirect('/welcome')
			else:
				error_registration = "Passwords do not match"
		elif username_registration or password_registration or password_check_registration:
			error_registration = "Invalid Registration"
		return error_registration