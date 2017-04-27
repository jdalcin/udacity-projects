from python.webpage_backend.webpage_handler import *

class PostInsertHandler(Handler):

	def post(self):
		super(PostInsertHandler, self).check_valid_user(self.logged_in_user)
		subject = self.request.get('subject')
		blog = self.request.get('blog')
		# if form is filled properly then redirect to blog page, else render an error
		if subject and blog: 
			# checks if form should be inserted into a pre-existing blog or a new blog
			if not self.request.get('blog-id'): # new blog
				BlogPost(parent = self.root_blog_key, user = self.logged_in_user, subject = subject, blog = blog, 
					    likes = 0, dislikes = 0).put() # creates new position for blog in database
			else: # pre-existing
				blog_id = int(self.request.get('blog-id'))
				super(PostInsertHandler, self).check_valid_blog_id(blog_id)
				blog_entity = BlogPost.get_by_id(blog_id, parent = self.root_blog_key) # gets blog from input clicked
				blog_entity.subject = self.request.get('subject')
				blog_entity.blog = self.request.get('blog')
				blog_entity.put() # add blog back to its original position in the database
			self.redirect('/blog')
		else:
			self.render('create-blog.html', username = self.logged_in_user, blog_id = self.request.get('blog-id'), subject = subject, blog = blog, error = "Invalid Post")