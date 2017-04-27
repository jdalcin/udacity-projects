from python.webpage_backend.webpage_handler import *

class BlogDeletePostHandler(Handler):

	def post(self):
		super(BlogDeletePostHandler, self).check_valid_user(self.logged_in_user)
		blog_id = int(self.request.get('blog-id'))
		super(BlogDeletePostHandler, self).check_valid_blog_id(blog_id)
		if super(BlogDeletePostHandler, self).check_user_owns_post(blog_id):
			BlogPost.get_by_id(blog_id, parent = self.root_blog_key).delete()
		self.redirect('/blog')