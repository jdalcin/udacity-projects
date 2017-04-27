from python.webpage_backend.webpage_handler import *

class CommentEditHandler(Handler):

	def post(self):
		super(CommentEditHandler, self).check_valid_user(self.logged_in_user)
		comment_id = int(self.request.get('comment-id'))
		super(CommentEditHandler, self).check_valid_comment_id(comment_id)
		comment_entity = Comment.get_by_id(comment_id, parent = self.root_comment_key)
		# allows comment chosen to be edited from blog page to render on comment creation page
		self.render('create-comment.html', username = self.logged_in_user, comment = comment_entity.comment, 
			        blog_id = comment_entity.blog_id, comment_id = comment_id) 