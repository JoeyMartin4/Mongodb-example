"""
A class representing a movie.

Attributes:
    title (str): The movie title.
    director (str): The movie director.
    release_year (int): The release year.
"""


class Movie:
    title = ""
    director = ""
    release_year = 0
    user_key = ""
    movie_id = ""
    movie_map = {}

    def __init__(self, title, director, release_year, user_key, movie_map):
        """
        Initialize a Movie with title, director, release year, and user_key.
        """
        self.title = title
        self.director = director
        self.release_year = release_year
        self.user_key = user_key
        movie_map[self.get_key()] = self
        self.movie_map = movie_map

    def __str__(self):
        """
        Return a string representation of the movie.
        """
        return (f"{self.title} ({self.release_year}), Directed by "
                f"{self.director}, owned by user {self.user_key}")

    def __repr__(self):
        """
        Return a detailed string representation of the movie.
        """
        return (f"Movie(title={self.title!r}, director={self.director!r}, "
                f"release_year={self.release_year!r}, user_key={self.user_key})")

    @classmethod
    def build(cls, movie_dict, movie_map):
        return Movie(
            movie_dict["title"],
            movie_dict["director"],
            movie_dict["year"],
            movie_dict["user_key"],
            movie_map
        )

    @classmethod
    def lookup(cls, key):
        lower_key = key.lower
        if lower_key in movie_map:
            return cls.movie_map[key]
        else:
            return None

    def to_dict(self):
        return {
            "_id": f"{self.get_key()}|{self.user_key}",
            "title": self.title,
            "director": self.director,
            "release_year": self.release_year,
            "user_key": self.user_key
        }

    def get_key(self):
        return f"{self.director}: {self.title}"

    def update(self, title, director, release_year, user_key, **kwargs):
        """
        Update the movie's title, director, and release year.

        Extra keyword arguments are ignored.
        """
        self.title = title
        self.director = director
        self.release_year = release_year
        self.user_key = user_key

