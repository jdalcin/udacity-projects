import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import jinja2
import webapp2
import hash 

from  database_entities import *

# webpage template using the Jinja environment
template_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
	"""Webpages inherit this class. Serves as the blueprint among which every webpage of this multi-user blog is built upon."""

	def __init__(self, request, response):
		webapp2.RequestHandler.__init__(self, request, response)
		self.logged_in_user = hash.validate(self.request.cookies.get('username'))
		self.blog_id = hash.validate(self.request.get('blog-id'))
		self.root_blog_key = db.Key.from_path('BlogPost', 'root_blog')
		self.root_comment_key = db.Key.from_path('Comment', 'root_comment')
		self.blog_posts = db.GqlQuery("SELECT * FROM BlogPost WHERE ANCESTOR IS :1 ORDER BY date DESC", 
						      self.root_blog_key)
		self.comments = db.GqlQuery("SELECT * FROM Comment WHERE ANCESTOR IS :1 ORDER BY date DESC", 
			                                     self.root_comment_key)

	def check_valid_user(self, name):
		if not name:
			self.redirect('/registration')

	def check_valid_blog_id(self, blog_id):
		blog_entity = BlogPost.get_by_id(blog_id, parent = self.root_blog_key)
		if not blog_entity:
			self.response.set_cookie('username', None, path='/')
			self.redirect('/registration')

	def check_valid_comment_id(self, comment_id):
		comment_entity = Comment.get_by_id(comment_id, parent = self.root_comment_key)
		if not comment_entity:
			self.response.set_cookie('username', None, path='/')
			self.redirect('/registration')

	def check_user_owns_comment(self, comment_id):
		comment_entity = Comment.get_by_id(comment_id, parent = self.root_comment_key)
		if comment_entity.user == self.logged_in_user:
			return True
		else:
			return False

	def check_user_owns_post(self, blog_id):
		blog_entity = BlogPost.get_by_id(blog_id, parent = self.root_blog_key)
		if blog_entity.user == self.logged_in_user:
			return True
		else:
			return False

	def render_string(self, template, **kwargs):
		t = jinja_env.get_template(template)
		return t.render(**kwargs)

	def render(self, template, **kwargs):
		self.response.out.write(self.render_string(template, **kwargs))
