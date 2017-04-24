from python.webpage_backend.webpage_handler import *

class CommentHandler(Handler):
	"""Webpage in which a comment is created."""

	def get(self):
		if self.logged_in_user:
			self.render('create-comment.html', username = self.logged_in_user, blog_id = self.request.get('blog-id'))
		else:
			self.redirect('/registration')

	def post(self):
		if self.logged_in_user:
			blog_id = self.request.get('blog-id')
			comment_id = self.request.get('comment-id')
			if blog_id: # run if input came from "create-comment.html"
				# if statements run based on which button on page "create-comment.html" was clicked
				if self.request.get('cancel'):
					self.redirect('/blog')
				elif self.request.get('submit-comment'): 
					blog_id = int(blog_id)
					comment = self.request.get('comment')
					if comment:
						#check if input is either for editing a pre-existing comment or creating a new one
						if self.request.get('is-edit'):
							comment_id = int(comment_id)
							comment_entity = Comment.get_by_id(comment_id, parent = self.root_comment_key)
							comment_entity.comment = comment
							comment_entity.put()
						else:
							Comment(parent = self.root_comment_key, user = self.logged_in_user, 
								     comment = comment, blog_id = blog_id).put() #puts comment in database 
						self.redirect('/blog')
					else:
						self.render('create-comment.html', username = self.logged_in_user, blog_id = blog_id, 
						                  error = "Missing comment") # error statement rendered when missing a comment upon 
						                                                             # submission
			elif comment_id: # run if input came from "blog-page.html"
				comment_id = int(comment_id)
				comment_entity = Comment.get_by_id(comment_id, parent = self.root_comment_key)
				# allows comment chosen to be edited from blog page to render on comment creation page
				self.render('create-comment.html', username = self.logged_in_user, comment = comment_entity.comment, 
					        blog_id = comment_entity.blog_id, comment_id = comment_id, is_edit = "true") 
		else:
			self.redirect('/registration')