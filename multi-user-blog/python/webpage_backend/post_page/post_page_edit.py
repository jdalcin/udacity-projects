from python.webpage_backend.webpage_handler import *

class PostEditHandler(Handler):

	def post(self):
		super(PostEditHandler, self).check_valid_user(self.logged_in_user)
		blog_id = int(self.request.get('blog-id'))
		super(PostEditHandler, self).check_valid_blog_id(blog_id)
		if not super(PostEditHandler, self).check_user_owns_post(blog_id):
			self.response.set_cookie('username', None, path='/')
			self.redirect('/registration') # this means user is not owner of post. The user tried to edit source code from the client side. Any user who does this is logged out and sent back to registration.
		blog_entity = BlogPost.get_by_id(blog_id, parent = self.root_blog_key) # gets blog from input clicked
		self.render('create-blog.html', subject = blog_entity.subject, blog = blog_entity.blog, blog_id = blog_id)
		