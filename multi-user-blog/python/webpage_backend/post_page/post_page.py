from python.webpage_backend.webpage_handler import *

class PostHandler(Handler):
	"""Webpage in which a new blog post is created."""

	def get(self):
		super(PostHandler, self).check_valid_user(self.logged_in_user)
		self.render('create-blog.html', username = self.logged_in_user)
