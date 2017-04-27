from python.webpage_backend.webpage_handler import *

class BlogDeleteCommentHandler(Handler):

	def post(self):
		comment_id = int(self.request.get('comment-id'))
		super(BlogDeleteCommentHandler, self).check_valid_comment_id(comment_id)
		Comment.get_by_id(comment_id, parent = self.root_comment_key).delete()
		self.redirect('/blog')