from python.webpage_backend.webpage_handler import *

class BlogPageHandler(Handler):
	"""Blog's Webpage"""

	def __init__(self, request, response):
		Handler.__init__(self, request, response)
		# gets blog posts and comments to display on the webpage
		self.blog_posts = db.GqlQuery("SELECT * FROM BlogPost WHERE ANCESTOR IS :1 ORDER BY date DESC", 
						      self.root_blog_key)
		self.comments = db.GqlQuery("SELECT * FROM Comment WHERE ANCESTOR IS :1 ORDER BY date DESC", 
			                                     self.root_comment_key)

	def get(self):
		if self.logged_in_user:	
			self.render('blog-page.html', username = self.logged_in_user, blog_posts = self.blog_posts, 
				       comments = self.comments)
		else:
			self.redirect('/registration')

	def post(self):
		if self.logged_in_user:
			blog_id = 0;
			blog_entity = None;
			comment_id = self.request.get('comment-id')
			blog_id = self.request.get('blog-id')
			error = ''
			if comment_id:
				comment_id = int(comment_id)
			if blog_id:
				blog_id = int(blog_id)
				blog_entity = BlogPost.get_by_id(blog_id, parent = self.root_blog_key) # gets blog from input clicked
			# if statements decide which button in the html documents was clicked
			# subsequently, a webpage is rendered based on the button clicked
			if self.request.get('logout'):
				self.response.set_cookie('username', None)
				self.redirect('/registration')
			elif self.request.get('delete-comment'):
				Comment.get_by_id(comment_id, parent = self.root_comment_key).delete()
				self.redirect('/blog')
			elif self.request.get('like') or self.request.get('dislike'):
				user_entity = User.get_by_key_name(self.logged_in_user) # gets user currently logged in
				if blog_id in user_entity.rated_blogs:
					error = "only one vote allowed"
				self.rate_post(user_entity, blog_entity, blog_id)
				self.render('blog-page.html', username = self.logged_in_user, blog_posts = self.blog_posts, comments = 
					self.comments, blog_id = blog_id, error = error)
			elif self.request.get('delete'):
				blog_entity.delete()
				self.redirect('/blog')
			elif self.request.get('edit'):
				self.render('create-blog.html', subject = blog_entity.subject, blog = blog_entity.blog, blog_id = blog_id)
		else:
			self.redirect('/registration')
		

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