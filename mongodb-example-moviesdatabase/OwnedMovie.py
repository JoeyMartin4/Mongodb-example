"""
A subclass of Movie representing an owned movie with a user key.

Attributes:
    title (str): The movie title.
    director (str): The movie director.
    release_year (int): The release year.
    user_key (str): The user key
"""

from Movie import Movie


class OwnedMovie(Movie):
    def __init__(self, title, director, release_year, user_key):
        """
        Initialize an OwnedMovie.
        """
        super().__init__(title, director, release_year, user_key)

    def __str__(self):
        """
        Return a string representation of the owned movie.
        """
        return (f"{self.title} ({self.release_year}), Directed by "
                f"{self.director}, Owned by {self.user_key}")

    def to_dict(self):
        dict = super().to_dict()
        dict["type"] = "OwnedMovie"
        return dict

    def __repr__(self):
        """
        Return a detailed string representation of the owned movie.
        """
        return (f"OwnedMovie(title={self.title!r}, director={self.director!r}, "
                f"release_year={self.release_year!r}, user_key="
                f"{self.user_key!r})")

    def update(self, title, director, release_year, **kwargs):
        """
        Update the owned movie's attributes.

        The keyword argument 'series_name' is used to update the series name.
        """
        super().update(title, director, release_year, **kwargs)
        if "series_name" in kwargs:
            self.series_name = kwargs["series_name"]
