from python.webpage_backend.webpage_handler import *

class RegistrationLoginHandler(Handler):

	def post(self):
		# 'registration.html' Form Information
		username_login = self.request.get('username-login')
		password_login = self.request.get('password-login')
		error_login = self.click_login(username_login, password_login)
		if error_login != '':
			self.render('registration.html', username_login = username_login, password_login = password_login, 
				        error_login = error_login)

	def click_login(self, username_login, password_login, error_login = ''):
		"""Checks if login information submitted is valid. If information is valid, user is logged in. If not, an error pops up."""

		if username_login and password_login and User.get_by_key_name(username_login):
			hashed_password = User.get_by_key_name(username_login).password
			#checks if password inputted is valid	
			if hash.validate_login(username_login, password_login, hashed_password):
				self.response.headers.add_header('Set-Cookie', 
					                                             'username={};Path=/'.format(hash.make_secure(
					                                              username_login.lower())))
				self.redirect('/welcome')
			else:
				error_login = "Invalid password"
		else:
			error_login = "Invalid login"
		return error_login