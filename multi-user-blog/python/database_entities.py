"""Entities (blog posts, comments of each blog, and registered users) inside the google app engine database."""

from google.appengine.ext import db

class BlogPost(db.Model):
	user = db.StringProperty(required = True)
	subject = db.StringProperty(required = True)
	blog = db.TextProperty(required = True)
	likes = db.IntegerProperty(required = True)
	dislikes = db.IntegerProperty(required = True)
	date = db.DateTimeProperty(auto_now_add = True)

class Comment(db.Model):
	user = db.StringProperty(required = True)
	blog_id = db.IntegerProperty(required = True)
	comment = db.TextProperty(required = True)
	date = db.DateTimeProperty(auto_now_add = True)


class User(db.Model):
	user = db.StringProperty(required = True)
	password = db.StringProperty(required = True)
	rated_blogs = db.ListProperty(int)
	comments = db.ListProperty(int)