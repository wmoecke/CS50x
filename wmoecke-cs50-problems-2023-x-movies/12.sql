SELECT m.title
FROM movies m
JOIN stars s ON s.movie_id = m.id
JOIN people p ON p.id = s.person_id
WHERE LOWER(p.name) IN ('johnny depp', 'helena bonham carter')
GROUP BY m.title
HAVING COUNT(m.title) >= 2;