SELECT m.title, m.year
FROM movies m
WHERE LOWER(m.title) LIKE 'harry potter%'
ORDER BY m.year ASC;