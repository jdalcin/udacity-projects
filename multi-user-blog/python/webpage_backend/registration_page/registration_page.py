from python.webpage_backend.webpage_handler import *

class RegistrationHandler(Handler):
	"""Webpage which allows a new user to register or an existing user to login into their blog."""

	def get(self):
		self.render('registration.html')


	

		
