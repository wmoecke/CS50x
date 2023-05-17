SELECT birth
FROM people
WHERE id = (SELECT p.id FROM people p WHERE LOWER(p.name) = 'emma stone');