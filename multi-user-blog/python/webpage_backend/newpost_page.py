from python.webpage_backend.webpage_handler import *

class NewPostHandler(Handler):
	"""Webpage in which a new blog post is created."""

	def get(self):
		if self.logged_in_user:
			self.render('create-blog.html', username = self.logged_in_user)
		else:
			self.redirect('/registration')

	def post(self):
		if self.logged_in_user:
			subject = self.request.get('subject')
			blog = self.request.get('blog')
			blog_id = self.request.get('edit')
			# runs a set of operations based on the button clicked for webpage "create-blog.html"
			if self.request.get('submit-blog'):
				# checks if a blog submitted is either new or pre-existing
				if subject and blog: # new blog
					BlogPost(parent = self.root_blog_key, user = self.logged_in_user, subject = subject, blog = blog, 
						    likes = 0, dislikes = 0).put() # creates new position for blog in database
					self.redirect('/blog')
				elif blog_id: # pre-existing blog
					blog_id = int(blog_id)
					blog_entity = BlogPost.get_by_id(blog_id, parent = self.root_blog_key)
					blog_entity.subject = subject
					blog_entity.blog = blog
					blog_entity.put() # add blog back to its original position in the database
					self.redirect('/blog')
				else:
					# renders if blog has not properly been filled out
					self.render('create-blog.html', username = self.logged_in_user, error = "Invalid Post") 
			elif self.request.get('cancel'):
				self.redirect('/blog')
		else:
			self.redirect('/registration')