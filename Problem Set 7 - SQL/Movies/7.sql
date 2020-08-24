SELECT movies.title, ratings.rating FROM movies
INNER JOIN ratings ON movies.id = ratings.movie_id
WHERE year = 2010 and ratings.rating > 0
GROUP BY movies.title
ORDER BY ratings.rating DESC, movies.title ASC;