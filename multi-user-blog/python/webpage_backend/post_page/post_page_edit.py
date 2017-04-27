from python.webpage_backend.webpage_handler import *

class PostEditHandler(Handler):

	def post(self):
		super(PostEditHandler, self).check_valid_user(self.logged_in_user)
		blog_id = int(self.request.get('blog-id'))
		super(PostEditHandler, self).check_valid_blog_id(blog_id)
		blog_entity = BlogPost.get_by_id(blog_id, parent = self.root_blog_key) # gets blog from input clicked
		self.render('create-blog.html', subject = blog_entity.subject, blog = blog_entity.blog, blog_id = blog_id)
		