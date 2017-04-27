#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from python.webpage_backend.webpage_handler import *

from python.webpage_backend.registration_page.registration_page import *
from python.webpage_backend.registration_page.registration_page_registerhandler import *
from python.webpage_backend.registration_page.registration_page_loginhandler import *

from python.webpage_backend.welcome_page.welcome_page import *

from python.webpage_backend.blog_page.blog_page import *
from python.webpage_backend.blog_page.blog_page_deletecomment import *
from python.webpage_backend.blog_page.blog_page_deletepost import *
from python.webpage_backend.blog_page.blog_page_ratepost import *
from python.webpage_backend.blog_page.blog_page_logout import *

from python.webpage_backend.post_page.post_page import *
from python.webpage_backend.post_page.post_page_edit import *
from python.webpage_backend.post_page.post_page_insert import *

from python.webpage_backend.comment_page.comment_page import *
from python.webpage_backend.comment_page.comment_page_edit import *
from python.webpage_backend.comment_page.comment_page_insert import *

class MainHandler(Handler):
	"""Starting webpage of the multi-user blog."""
	
	def get(self):
		self.redirect('/welcome')

# creates webpages
app = webapp2.WSGIApplication([
	('/', MainHandler), 
	('/welcome', WelcomeHandler), 
	('/registration', RegistrationHandler), 
	('/registration/login', RegistrationLoginHandler),
	('/registration/register', RegistrationRegisterHandler),
	('/blog', BlogPageHandler), 
	('/blog/delete-post', BlogDeletePostHandler),
	('/blog/delete-comment', BlogDeleteCommentHandler),
	('/blog/rate-post', BlogRatePostHandler),
	('/blog/logout', BlogLogoutHandler),
	('/post', PostHandler), 
	('/post/edit', PostEditHandler),
	('/post/insert', PostInsertHandler),
	('/comment', CommentHandler),
	('/comment/edit', CommentEditHandler),
	('/comment/insert', CommentInsertHandler)], 
	debug=True)

