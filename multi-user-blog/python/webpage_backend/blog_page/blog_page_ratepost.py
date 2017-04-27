from python.webpage_backend.webpage_handler import *

class BlogRatePostHandler(Handler):

	def post(self):
		super(BlogRatePostHandler, self).check_valid_user(self.logged_in_user)
		blog_id = int(self.request.get('blog-id'))
		super(BlogRatePostHandler, self).check_valid_blog_id(blog_id)
		if super(BlogRatePostHandler, self).check_user_owns_post(blog_id):
			self.response.set_cookie('username', None, path='/')
			self.redirect('/registration') # this means user owns post he tried to rate and attempted to alter source code from client side. Any user who does this is logged out and sent back to registration.
		blog_entity = BlogPost.get_by_id(blog_id, parent = self.root_blog_key) # gets blog from input clicked
		user_entity = User.get_by_key_name(self.logged_in_user) # gets user currently logged in
		error = ''
		if blog_id in user_entity.rated_blogs:
			error = "only one vote allowed"
		self.rate_post(user_entity, blog_entity, blog_id)
		if error != '':
			self.render('blog-page.html', username = self.logged_in_user, blog_posts = self.blog_posts, comments = 
				self.comments, blog_id = blog_id, error = error)
		else:
			self.redirect('/blog')

	def rate_post(self, user_entity, blog_entity, blog_id):
		"""rates the blog post clicked if it has yet to be rated"""
		if len(user_entity.rated_blogs) == 0 or not blog_id in user_entity.rated_blogs:
				if self.request.get('like'):
					blog_entity.likes += 1
				elif self.request.get('dislike'):
					blog_entity.dislikes += 1
				user_entity.rated_blogs.append(blog_id)
				user_entity.put()
				blog_entity.put()