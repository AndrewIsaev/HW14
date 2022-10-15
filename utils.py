import json
import sqlite3

from config.config import DATA_BASE


def query_to_db(sql_query: str) -> list[dict]:
    """
    Connect with db and return response
    :param sql_query: string with query on SQL
    :return: list with items` dicts
    """

    # Open db
    with sqlite3.connect(DATA_BASE) as con:
        # Create cursor
        cur = con.cursor()
        sqlite_query = sql_query
        cur.execute(sqlite_query)
        return cur.fetchall()


def search_movie_by_title(user_title: str) -> dict | str:
    """
    Search movies by title
    :param user_title: film title
    :return: dict with title, country, release_year, genre, description or string if film not found
    """
    # Create sql query
    sql_query = f"""
                SELECT title, country, release_year, listed_in, description
                FROM netflix
                WHERE title = '{user_title}'
    """
    # Get response
    response = query_to_db(sql_query)
    # Check Exception if film not found
    try:
        title, country, release_year, listed_in, description = response[0]
    except IndexError:
        return "Film not found"
    else:
        result = {
            "title": title,
            "country": country,
            "release_year": release_year,
            "genre": listed_in,
            "description": description
        }
    return result


def search_between_years(start_year: int, stop_year: int) -> list[dict] | str:
    """
    Search films between two years
    :param start_year: year from which start searching
    :param stop_year: year to which stop searching
    :return: list with films` dicts
    """
    sqlite_query = f"""
        SELECT title, release_year
        FROM netflix
        WHERE release_year BETWEEN {start_year} AND {stop_year}
        LIMIT 100
    """
    # Get response
    response = query_to_db(sqlite_query)
    result_list = []
    for item in response:
        film = {
            "title": item[0],
            "release_year": item[1]
        }
        result_list.append(film)
    # Check if not any films between years
    if not result_list:
        return "Films not found"
    return result_list


def search_by_rating(user_rating: str) -> list[dict]:
    """
    Search films by rating
    :param user_rating: children, family or adult
    :return:
    """
    # Create dict with rating groups
    rating = {
        "children": ('G', 'G'),
        "family": ('G', 'PG', 'PG-13'),
        "adult": ('R', 'NC-17')
    }

    sql_query = f"""
                    SELECT title, rating, description
                    FROM netflix
                    WHERE rating IN {rating[user_rating]}
    """
    # Get response
    response = query_to_db(sql_query)
    result = []
    for item in response:
        film = {
            "title": item[0],
            "rating": item[1],
            "description": item[2]
        }
        result.append(film)
    return result


def get_last_ten_films_by_genre(genre: str) -> list[dict]:
    """
    Search last ten films by genre
    :param genre: Films genre
    :return: Last ten films with current genre
    """
    sql_query = f"""
                SELECT title, description
                FROM netflix
                WHERE listed_in LIKE '%{genre}%'
                AND type = 'Movie'
                ORDER BY release_year DESC 
                LIMIT 10
    """
    # Get response
    response = query_to_db(sql_query)
    result = []
    for item in response:
        film = {
            "title": item[0],
            "description": item[1]
        }
        result.append(film)
    return result


def get_actors_which_played_more_then_two(actor1: str, actor2: str) -> list:
    """
    Search actors which take part with users actors more than two times
    :param actor1: Actor 1 name
    :param actor2: Actor 2 name
    :return: List with actors who takes part with users actors more than two times
    """
    sql_query = f"""
        SELECT title, "cast"
        FROM netflix
        WHERE "cast" LIKE '%{actor1}%'
        AND "cast" LIKE '%{actor2}%'
        """
    # Get response
    response = query_to_db(sql_query)
    # Create list with all actors in finding films
    all_actors = []
    for items in response:
        actor_list = items[1].split(", ")
        all_actors.extend(actor_list)

    # Search who take part more than two times
    more_twice_list = []
    for actor in set(all_actors):
        if all_actors.count(actor) > 2 and actor not in (actor1, actor2):
            more_twice_list.append(actor)
    return more_twice_list


def get_films_by_type_year_genre(film_type: str, release_year: int, genre: str) -> json:
    """
    Search films by type, release year, genre
    :param film_type: Movie or TV Show
    :param release_year: release year
    :param genre: film`s genre
    :return: json with films data
    """
    sql_query = f"""
                SELECT title, description
                FROM netflix
                WHERE type = '{film_type.title()}'
                AND release_year = {release_year}
                AND listed_in LIKE '%{genre}%'
    """
    # Get response
    response = query_to_db(sql_query)
    result = []
    for item in response:
        film = {
            "title": item[0],
            "description": item[1]
        }
        result.append(film)
    return json.dumps(result, indent=4, ensure_ascii=False)
