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
import os
import webapp2
import jinja2

# webpage template using the Jinja environment
template_dir = os.path.join(os.path.dirname(__file__))
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)


class Handler(webapp2.RequestHandler):
	"""Webpages inherit this class. Serves as the blueprint among which every webpage of this multi-user blog is built upon."""

	def render_string(self, template, **kwargs):
		t = jinja_env.get_template(template)
		return t.render(**kwargs)

	def render(self, template, **kwargs):
		self.response.out.write(self.render_string(template, **kwargs))


class MainHandler(Handler):
	def get(self):
		self.render('index.html')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
], debug=True)
