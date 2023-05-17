SELECT m.title
FROM movies m
JOIN ratings r ON r.movie_id = m.id
JOIN stars s ON s.movie_id = r.movie_id
JOIN people p ON p.id = s.person_id
WHERE LOWER(p.name) = 'chadwick boseman'
ORDER BY r.rating DESC
LIMIT 5;