import os
import configparser
from pymongo import MongoClient
from User import User
from Movie import Movie
from MovieGenre import MovieGenre
from flask import session


class Database:
    def __init__(cls):
        cls.client = None
        cls.db = None
        cls.movies = None
        cls.genres = None
        cls.users = None
        cls.connect()

    @classmethod
    def connect(cls):
        """Establishes a connection to the MongoDB database using config file."""
        home_dir = os.environ.get("USERPROFILE", os.environ.get("HOME"))
        config_dir = os.path.join(home_dir, "movie_manager")
        config_file = os.path.join(config_dir, "movie_manager.ini")
        config = configparser.ConfigParser()
        config.read(config_file)
        username = config.get("database", "username")
        password = config.get("database", "password")
        db_name = config.get("database", "db_name")
        connection_string = (f"mongodb+srv://{username}:{password}"
                             "@projectcluster.e9s9m.mongodb.net/"
                             f"?retryWrites=true&w=majority&appName=ProjectCluster")
        cls.client = MongoClient(connection_string)
        cls.db = cls.client[db_name]
        cls.movies = cls.db["movies"]
        cls.genres = cls.db["genres"]
        cls.users = cls.db["users"]

    @classmethod
    def reconnect(cls):
        """Reconnects to the MongoDB database."""
        if cls.client:
            cls.client.close()
        cls.connect()


    @classmethod
    def rebuild_database(cls):
        # Connect to database
        Database.connect()

        """Clears and rebuilds the database with sample data."""
        cls.movies.drop()
        cls.genres.drop()

        # Sample movies, including OwnedMovie and MovieGenre instances
        sample_movies = [
            {
                "title": "Inception",
                "director": "Christopher Nolan",
                "year": 2010,
                "user_key": "marc"
             },
            {
                "title": "The Matrix",
                "director": "Wachowskis",
                "year": 1999,
                "user_key": "marc"
            },
            {
                "title": "Howl's Moving Castle",
                "director": "Hayao Miyazaki",
                "year": 2004,
                "user_key": "testinguser"
            }
        ]
        cls.movies.insert_many(sample_movies)

        # genres: All Movies, Sci-Fi, Fantasy
        genres = [
            {
                "name": "All Movies",
                "description": "genre with all movies.",
                "movies": [movie["title"] for movie in sample_movies],
                "user_key": "marc"
            },
            {
                "name": "All Movies",
                "description": "genre with all movies.",
                "movies": [movie["title"] for movie in sample_movies],
                "user_key": "alice"
            },
            {
                "name": "All Movies",
                "description": "genre with all movies.",
                "movies": [movie["title"] for movie in sample_movies],
                "user_key": "testinguser"
            },
            {
                "name": "Sci-Fi",
                "description": "Science fiction movies.",
                "movies": ["Inception", "The Matrix"],
                "user_key": "marc"
            },
            {
                "name": "Fantasy",
                "description": "Fantasy-themed movies.",
                "movies": ["Howl's Moving Castle"],
                "user_key": "marc"
            }
        ]
        cls.genres.insert_many(genres)
        print("Database rebuilt with sample data.")

    @classmethod
    def get_user(cls):
        if "user" in session:
            return session["user"]
        return None

    @classmethod
    def get_user_key(cls):
        gotten_user = cls.get_user()
        if gotten_user is None:
            return None
        return gotten_user.lower()

    @classmethod
    def read_movies(cls):
        """Returns a list of all movie documents."""
        return list(cls.movies.find())

    @classmethod
    def read_user_movies(cls, user_key):
        """Returns a list of all movie documents for the user."""
        return list(cls.movies.find({"user_key": user_key}))

    @classmethod
    def read_genres(cls):
        """Returns a list of all genre documents."""
        return list(cls.genres.find())

    @classmethod
    def read_user_genres(cls, user_key):
        """Returns a list of all genre documents for the user."""
        return list(cls.genres.find({"user_key": user_key}))

    @classmethod
    def login_user(cls, user):
        session["user"] = user.username


    @classmethod
    def read_data(cls, user_key):
        movie_map = {}
        movie_dicts = cls.read_user_movies(user_key)
        movie_map = [Movie.build(movie_dict, movie_map) for movie_dict in movie_dicts]


        genre_map = {}
        genre_dicts = cls.read_user_genres(user_key)
        genre_map = [MovieGenre.build(genre_dict, genre_map, movie_dicts) for genre_dict in genre_dicts]

        return movie_dicts, genre_dicts, movie_map, genre_map

    @classmethod
    def read_user(cls, user_key):
        cls.connect()
        user_dict = cls.users.find_one({'user_key': user_key.lower()})
        if user_dict is None:
            return None
        else:
            return User.build(user_dict)

    @classmethod
    def add_movie(cls, movie_data):
        """
        Adds a new movie to the database.
        movie_data: dict with movie details.
        """
        result = cls.movies.insert_one(movie_data)
        
        return result.inserted_id

    @classmethod
    def update_movie(cls, movie_title, updated_data, user_key):
        """
        Updates an existing movie by title.
        updated_data: dict with updated fields.
        """
        result = cls.movies.update_one(
            {"title": movie_title, "user_key": user_key},
            {"$set": updated_data}
        )
        
        return result.modified_count

    @classmethod
    def add_genre(cls, genre_data):
        """
        Adds a new genre to the database.
        genre_data: dict with genre details.
        """
        user_key = Database.get_user_key()
        result = cls.genres.insert_one({"name": genre_data, "movies": [], "user_key": user_key})
        
        return result.inserted_id

    @classmethod
    def delete_genre(cls, genre_name):
        """Deletes a genre by name."""
        user_key = Database.get_user_key()
        result = cls.genres.delete_one({"name": genre_name, "user_key": user_key})
        
        return result.deleted_count

    @classmethod
    def add_movie_to_genre(cls, genre_name, movie_title, user_key):
        """
        Adds a movie to a genre's movie list.
        Uses $addToSet to prevent duplicates.
        """
        result = cls.genres.update_one(
            {"name": genre_name, "user_key": user_key},
            {"$addToSet": {"movies": movie_title}}
        )
        
        return result.modified_count

    @classmethod
    def update_genre_name(cls, genre_name, new_genre_name, user_key):
        """
        updates a genre's name
        Uses $addToSet to prevent duplicates.
        """
        result = cls.genres.update_one(
            {"name": genre_name, "user_key": user_key},
            {"$set": {"name": new_genre_name}}
        )
        
        return result.modified_count

    @classmethod
    def remove_movie_from_genre(cls, genre_name, movie_title, user_key):
        """
        Removes a movie from a genre's movie list.
        """
        result = cls.genres.update_one(
            {"name": genre_name, "user_key": user_key},
            {"$pull": {"movies": movie_title}}
        )
        
        return result.modified_count


    @classmethod
    def add_owned_movie(cls, title, director, year, user_key):
        """
        Adds a new OwnedMovie to the database.
        """
        movie_data = {
            "title": title,
            "director": director,
            "year": int(year),
            "user_key": user_key
        }
        
        return cls.add_movie(movie_data)

    @classmethod
    def add_movie_genre(cls, genre_name, description, user_key, movies=None):
        """
        Adds a new MovieGenre to the database.
        """
        if movies is None:
            movies = []
        genre_data = {
            "name": genre_name,
            "description": description,
            "movies": movies,
            "user_key": user_key
        }
        
        return cls.add_genre(genre_data)


if __name__ == "__main__":
    db = Database()
    db.rebuild_database()
