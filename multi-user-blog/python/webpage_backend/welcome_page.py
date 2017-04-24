from python.webpage_backend.webpage_handler import *

class WelcomeHandler(Handler):
	"""Webpage which welcomes the user into the blog."""

	def get(self):
		# sends user to the blog if their cookie is recognized, otherwise, sends user back to registration
		if self.logged_in_user:
			self.render('welcome.html', username = self.logged_in_user)
		else:
			self.redirect('/registration')