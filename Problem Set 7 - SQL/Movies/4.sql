SELECT count(id) from movies
JOIN ratings ON movies.id = ratings.movie_id
WHERE ratings.rating = 10.0;