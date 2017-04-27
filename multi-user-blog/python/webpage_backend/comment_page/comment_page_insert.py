from python.webpage_backend.webpage_handler import *

class CommentInsertHandler(Handler):

	def post(self):
		super(CommentInsertHandler, self).check_valid_user(self.logged_in_user)
		blog_id = int(self.request.get('blog-id'))
		super(CommentInsertHandler, self).check_valid_blog_id(blog_id)
		comment = self.request.get('comment')
		# check if form properly filled
		if comment: # properly filled form
			#check if insert is updating a pre-existing comment or creating a new one
			if not self.request.get('comment-id'): # new comment
				Comment(parent = self.root_comment_key, user = self.logged_in_user, 
					     comment = comment, blog_id = blog_id).put() #puts comment in database
			else: # updating old comment
				comment_id = int(self.request.get('comment-id'))
				super(CommentInsertHandler, self).check_valid_comment_id(comment_id)
				if not super(CommentInsertHandler, self).check_user_owns_comment(comment_id):
					self.response.set_cookie('username', None, path='/')
					self.redirect('/registration')
				comment_entity = Comment.get_by_id(comment_id, parent = self.root_comment_key)
				comment_entity.comment = comment
				comment_entity.put()
			self.redirect('/blog')
		else: # improperly filled
			self.render('create-comment.html', username = self.logged_in_user, blog_id = blog_id, comment_id = self.request.get(       'comment-id'), comment = comment, error = "Missing comment") # error statement rendered when missing a comment upon submission