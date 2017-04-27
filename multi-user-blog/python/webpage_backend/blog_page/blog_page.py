from python.webpage_backend.webpage_handler import *

class BlogPageHandler(Handler):
	"""Blog's Webpage"""

	def get(self):
		super(BlogPageHandler, self).check_valid_user(self.logged_in_user)
		self.render('blog-page.html', username = self.logged_in_user, blog_posts = self.blog_posts, 
				       comments = self.comments)


		

	