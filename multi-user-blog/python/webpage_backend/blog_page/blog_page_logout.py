from python.webpage_backend.webpage_handler import *

class BlogLogoutHandler(Handler):

	def post(self):
		self.response.set_cookie('username', None, path='/')
		self.redirect('/registration')