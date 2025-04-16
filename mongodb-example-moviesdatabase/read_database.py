import sqlite3
from Movie import Movie
from OwnedMovie import OwnedMovie
from MovieGenre import MovieGenre

def load_movies():
    """Retrieve movies from the database."""
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    cursor.execute("SELECT title, director, release_year FROM movies")
    movies = [Movie(title, director, release_year) for title, director, release_year in cursor.fetchall()]
    conn.close()
    return movies

def load_owned_movies():
    """Retrieve owned movies from the database."""
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    cursor.execute("SELECT title, director, release_year, series_name FROM owned_movies")
    owned_movies = [OwnedMovie(title, director, release_year, series_name) for
                    title, director, release_year, series_name in cursor.fetchall()]
    conn.close()
    return owned_movies

def load_categories():
    """Retrieve categories from the database."""
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM categories")
    categories = [MovieGenre(name) for (name,) in cursor.fetchall()]
    conn.close()
    return categories
