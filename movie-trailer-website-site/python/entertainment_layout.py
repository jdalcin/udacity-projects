import media
import fresh_tomatoes

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

# prints movies on webpage
fresh_tomatoes.open_movies_page(movies)