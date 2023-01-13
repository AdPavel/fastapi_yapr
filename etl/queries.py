modified_movies_query = """
    SELECT fw.id,
    fw.rating AS imdb_rating,
    ARRAY_AGG(DISTINCT g.name) AS genre,
    fw.title,
    fw.description,
    ARRAY_AGG(DISTINCT p.full_name)
    FILTER(WHERE pfw.role = 'director') AS director,
    ARRAY_AGG(DISTINCT p.full_name)
    FILTER(WHERE pfw.role = 'actor') AS actors_names,
    ARRAY_AGG(DISTINCT p.full_name)
    FILTER(WHERE pfw.role = 'writer') AS writers_names,
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

sql_queries = {
    'movies': {
        'query': modified_movies_query,
        'variables_amount': 3
    },
    'genres': {
        'query': modified_genres_query,
        'variables_amount': 1
    }
}