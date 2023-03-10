modified_movies_query = """
    SELECT fw.id,
    fw.rating AS imdb_rating,
    JSON_AGG(DISTINCT jsonb_build_object('id', g.id, 'name', g.name)) AS genre,
    fw.title,
    fw.description,
    ARRAY_AGG(DISTINCT p.full_name)
    FILTER(WHERE pfw.role = 'director') AS directors_names,
    ARRAY_AGG(DISTINCT p.full_name)
    FILTER(WHERE pfw.role = 'actor') AS actors_names,
    ARRAY_AGG(DISTINCT p.full_name)
    FILTER(WHERE pfw.role = 'writer') AS writers_names,
    JSON_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name))
    FILTER(WHERE pfw.role = 'director') AS directors,
    JSON_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name))
    FILTER(WHERE pfw.role = 'actor') AS actors,
    JSON_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name))
    FILTER(WHERE pfw.role = 'writer') AS writers
    FROM content.film_work fw
    LEFT OUTER JOIN content.genre_film_work gfw ON (fw.id = gfw.film_work_id)
    LEFT OUTER JOIN content.genre g ON (gfw.genre_id = g.id)
    LEFT OUTER JOIN content.person_film_work pfw ON (fw.id = pfw.film_work_id)
    LEFT OUTER JOIN content.person p ON (pfw.person_id = p.id)
    WHERE fw.modified > %s OR p.modified > %s OR g.modified > %s
    GROUP BY fw.id;
"""
modified_genres_query = """
    SELECT id, name, description, modified
    FROM content.genre
    WHERE modified > %s;
"""
modified_persons_query = """
    SELECT p.id,
    p.full_name as name,
    ARRAY_AGG(DISTINCT pfw.role) AS role,
    ARRAY_AGG(DISTINCT pfw.film_work_id) AS film_ids
    FROM content.person p
    LEFT OUTER JOIN content.person_film_work pfw ON (p.id = pfw.person_id)
    WHERE p.modified > %s OR pfw.created > %s
    GROUP BY p.id;
"""


sql_queries = {
    'movies': {
        'query': modified_movies_query,
        'variables_amount': 3
    },
    'genres': {
        'query': modified_genres_query,
        'variables_amount': 1
    },
    'persons': {
        'query': modified_persons_query,
        'variables_amount': 2
    }
}