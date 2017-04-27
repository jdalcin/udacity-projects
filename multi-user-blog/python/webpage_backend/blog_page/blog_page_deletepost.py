from python.webpage_backend.webpage_handler import *

class BlogDeletePostHandler(Handler):

	def post(self):
		blog_id = int(self.request.get('blog-id'))
		super(BlogDeletePostHandler, self).check_valid_blog_id(blog_id)
		blog_entity = BlogPost.get_by_id(blog_id, parent = self.root_blog_key) # gets blog from input clicked
		blog_entity.delete()
		self.redirect('/blog')