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
		self.logged_in_user = hash.validate_cookie(self.request.cookies.get('username'))
		self.root_blog_key = db.Key.from_path('BlogPost', 'root_blog')
		self.root_comment_key = db.Key.from_path('Comment', 'root_comment')

	def render_string(self, template, **kwargs):
		t = jinja_env.get_template(template)
		return t.render(**kwargs)

	def render(self, template, **kwargs):
		self.response.out.write(self.render_string(template, **kwargs))