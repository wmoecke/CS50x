SELECT DISTINCT(p.name)
FROM people p
JOIN stars s ON s.person_id = p.id
WHERE s.movie_id IN (SELECT movie_id FROM stars WHERE person_id = (SELECT id from people WHERE LOWER(name) = 'kevin bacon' AND birth = 1958))
AND p.id != (SELECT id from people WHERE LOWER(name) = 'kevin bacon' AND birth = 1958);