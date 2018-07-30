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

from python import media
import webapp2
import os
import re

# Styles and scripting for the page
main_page_head = '''
<head>
    <meta charset="utf-8">
    <title>Fresh Tomatoes!</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <link rel="stylesheet" href="css/main.css">
    <script src="https://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <script src="js/main.js"></script>
</head>
'''

# The main page layout and title bar
main_page_content = '''
<!DOCTYPE html>
<html lang="en">
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>

    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <a class="navbar-brand" href="#">Fresh Tomatoes Movie Trailers</a>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
      {movie_tiles}
    </div>
  </body>
</html>
'''

# A single movie entry html template
movie_tile_content = '''
<div class="col-md-6 col-lg-4 movie-tile text-center" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
    <img src="{poster_image_url}" width="220" height="342">
    <h2>{movie_title}</h2>
</div>
'''

# creates movies
matrix = media.Movie("The Matrix", "https://upload.wikimedia.org/wikipedia/en/9/9a/The_Matrix_soundtrack_cover.jpg",
                     "https://www.youtube.com/watch?v=vKQi3bBA1y8")
lord_of_the_rings = media.Movie("Lord of the Rings: Return of the King", "http://static.rogerebert.com/uploads/movie/movie_poster/lord-of-the-rings-the-return-of-the-king-2003/large_j6NCjU6Zh7SkfIeN5zDaoTmBn4m.jpg",
                                "https://www.youtube.com/watch?v=r5X-hFf6Bwo")
spongebob_squarepants = media.Movie("The Spongebob Squarepants Movie", "https://upload.wikimedia.org/wikipedia/en/3/31/The_SpongeBob_SquarePants_Movie_poster.jpg",
                                    "https://www.youtube.com/watch?v=Tv8xk7BKaNM")
saving_private_ryan = media.Movie("Saving Private Ryan", "https://upload.wikimedia.org/wikipedia/en/a/ac/Saving_Private_Ryan_poster.jpg",
                                  "https://www.youtube.com/watch?v=zwhP5b4tD6g")
legend_of_zelda_breath_of_the_wild = media.Movie("The Legend of Zelda: Breath of the Wild", "http://www.siliconera.com/wordpress/wp-content/uploads/2018/03/DXUvxpyU0AAOquu_thumb.jpg",
                                                 "https://www.youtube.com/watch?v=zw47_q9wbBE")
matt_damon = media.Movie("Matt Damon", "https://metrouk2.files.wordpress.com/2014/03/wpid-article-1273762615545-0640082d000005dc-993038_636x820.jpg",
                         "https://www.youtube.com/watch?v=PkjLMWS3U4Q")

movies = [matrix, lord_of_the_rings, spongebob_squarepants, saving_private_ryan,
          legend_of_zelda_breath_of_the_wild, matt_damon]

class MainHandler(webapp2.RequestHandler):
	def get(self):
		# Replace the placeholder for the movie tiles with the actual dynamically generated content
  		rendered_content = main_page_content.format(movie_tiles=self.create_movie_tiles_content(movies))
		self.response.out.write(main_page_head + rendered_content)

	def create_movie_tiles_content(self, movies):
		# The HTML content for this section of the page
		content = ''
		for movie in movies:
			# Extract the youtube ID from the url
			youtube_id_match = re.search(r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
			youtube_id_match = youtube_id_match or re.search(r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
			trailer_youtube_id = youtube_id_match.group(0) if youtube_id_match else None
			# Append the tile for the movie with its content filled in
			content += movie_tile_content.format(
			movie_title=movie.title,
			poster_image_url=movie.poster_image_url,
			trailer_youtube_id=trailer_youtube_id
			)
		return content

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
