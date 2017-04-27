from python.webpage_backend.webpage_handler import *

class CommentHandler(Handler):
	"""Webpage in which a comment is created."""

	def get(self):
		super(CommentHandler, self).check_valid_user(self.logged_in_user)
		super(CommentHandler, self).check_valid_blog_id(int(self.request.get('blog-id')))
		self.render('create-comment.html', username = self.logged_in_user, blog_id = self.request.get('blog-id'))

	