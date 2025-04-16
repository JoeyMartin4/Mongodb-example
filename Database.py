import os
import configparser
from pymongo import MongoClient

class Database:
    def __init__(self):
        self.client = None
        self.db = None
        self.movies = None
        self.genres = None
        self.users = None
        self.connect()

    def connect(self):
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
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        self.movies = self.db["movies"]
        self.genres = self.db["genres"]
        self.users = self.db["users"]

    def reconnect(self):
        """Reconnects to the MongoDB database."""
        if self.client:
            self.client.close()
        self.connect()

    def rebuild_database(self):
        """Clears and rebuilds the database with sample data."""
        self.movies.drop()
        self.genres.drop()

        # Sample movies, including OwnedMovie and MovieGenre instances
        sample_movies = [
            {"title": "Inception", "director": "Christopher Nolan",
             "year": 2010, "genre": "Sci-Fi", "owner": "Alice",
             "series_name": "Dream Saga"},
            {"title": "The Matrix", "director": "Wachowskis",
             "year": 1999, "genre": "Sci-Fi", "owner": "Bob",
             "series_name": "Matrix Trilogy"},
            {"title": "Howl's Moving Castle", "director": "Hayao Miyazaki",
             "year": 2004, "genre": "Fantasy", "owner": "Alice",
             "series_name": "Ghibli Fantasy"}
        ]
        self.movies.insert_many(sample_movies)

        # genres: All Movies, Sci-Fi, Fantasy
        genres = [
            {
                "name": "All Movies",
                "description": "genre with all movies.",
                "movies": [movie["title"] for movie in sample_movies]
            },
            {
                "name": "Sci-Fi",
                "description": "Science fiction movies.",
                "movies": ["Inception", "The Matrix"]
            },
            {
                "name": "Fantasy",
                "description": "Fantasy-themed movies.",
                "movies": ["Howl's Moving Castle"]
            }
        ]
        self.genres.insert_many(genres)
        print("Database rebuilt with sample data.")

    def read_movies(self):
        """Returns a list of all movie documents."""
        return list(self.movies.find())

    def read_genres(self):
        """Returns a list of all genre documents."""
        return list(self.genres.find())

    def add_movie(self, movie_data):
        """
        Adds a new movie to the database.
        movie_data: dict with movie details.
        """
        result = self.movies.insert_one(movie_data)
        return result.inserted_id

    def update_movie(self, movie_title, updated_data):
        """
        Updates an existing movie by title.
        updated_data: dict with updated fields.
        """
        result = self.movies.update_one(
            {"title": movie_title},
            {"$set": updated_data}
        )
        return result.modified_count

    def add_genre(self, genre_data):
        """
        Adds a new genre to the database.
        genre_data: dict with genre details.
        """
        result = self.genres.insert_one(genre_data)
        return result.inserted_id

    def delete_genre(self, genre_name):
        """Deletes a genre by name."""
        result = self.genres.delete_one({"name": genre_name})
        return result.deleted_count

    def add_movie_to_genre(self, genre_name, movie_title):
        """
        Adds a movie to a genre's movie list.
        Uses $addToSet to prevent duplicates.
        """
        result = self.genres.update_one(
            {"name": genre_name},
            {"$addToSet": {"movies": movie_title}}
        )
        return result.modified_count

    def remove_movie_from_genre(self, genre_name, movie_title):
        """
        Removes a movie from a genre's movie list.
        """
        result = self.genres.update_one(
            {"name": genre_name},
            {"$pull": {"movies": movie_title}}
        )
        return result.modified_count

    def add_owned_movie(self, title, director, year, genre, owner, series_name):
        """
        Adds a new OwnedMovie to the database.
        """
        movie_data = {
            "title": title,
            "director": director,
            "year": year,
            "genre": genre,
            "owner": owner,
            "series_name": series_name
        }
        return self.add_movie(movie_data)

    def add_movie_genre(self, genre_name, description, movies=None):
        """
        Adds a new MovieGenre to the database.
        """
        if movies is None:
            movies = []
        genre_data = {
            "name": genre_name,
            "description": description,
            "movies": movies
        }
        return self.add_genre(genre_data)

if __name__ == "__main__":
    db = Database()
    db.rebuild_database()
