from python.webpage_backend.webpage_handler import *

class CommentEditHandler(Handler):

	def post(self):
		super(CommentEditHandler, self).check_valid_user(self.logged_in_user)
		comment_id = int(self.request.get('comment-id'))
		super(CommentEditHandler, self).check_valid_comment_id(comment_id)
		if not super(CommentEditHandler, self).check_user_owns_comment(comment_id):
			self.response.set_cookie('username', None, path='/')
			self.redirect('/registration') # this means user does not owner of comment he tried to edit and attempted to alter source code from client side. Any user who does this is logged out and sent back to registration.
		comment_entity = Comment.get_by_id(comment_id, parent = self.root_comment_key)
		# allows comment chosen to be edited from blog page to render on comment creation page
		self.render('create-comment.html', username = self.logged_in_user, comment = comment_entity.comment, 
			        blog_id = comment_entity.blog_id, comment_id = comment_id) 