"""
A class representing a movie category or genre.

Attributes:
    name (str): The name of the genre.
    items (list): A list of Movie or OwnedMovie objects.
    user_key (str): the user key for the genre
"""


class MovieGenre:
 #   All_Movies = "All Movies"
    name = ""
    items = []
    user_key = ""
    __map = {}

    def __init__(self, name, movie_dicts, user_key, genre_map):
        """
        Initialize a MovieGenre with a genre name and user key.
        """
        self.name = name
        self.items = movie_dicts
        self.user_key = user_key
        genre_map[self.get_key()] = self

    def to_dict(self):
        return{
            "id": self.get_key(),
            "name": self.name,
            "items": self.items,
            "user_key": self.user_key
        }

    @classmethod
    def build(cls, genre_dict, genre_map, movie_dicts):
        from Movie import Movie
        return MovieGenre(
            genre_dict["name"],
            # movie_dicts,
            [movie for movie in movie_dicts if movie["title"] in genre_dict["movies"]],
            genre_dict["user_key"],
            genre_map,
        )

    def get_key(self):
        return self.name.lower()

    def __str__(self):
        """
        Return a string representation of the genre.
        """
        return f"{self.name}"

    def __repr__(self):
        """
        Return a detailed string representation of the genre.
        """
        return (f"MovieGenre(name={self.name!r}, items="
                f"{len(self.items)} items)")

    def add(self, item):
        """
        Add a movie to the genre.
        """
        if item not in self.items:
            self.items.append(item)

    def remove(self, item):
        """
        Remove a movie from the genre.
        """
        if item in self.items:
            self.items.remove(item)

    def __iter__(self):
        """
        Allow iteration over the movies in the genre.
        """
        return iter(self.items)

    def __add__(self, other):
        """
        Combine two genres into a new genre.
        """
        combined_name = f"{self.name}/{other.name}"
        combined_genre = MovieGenre(combined_name, user_key)
        combined_genre.items = self.items + other.items
        return combined_genre
