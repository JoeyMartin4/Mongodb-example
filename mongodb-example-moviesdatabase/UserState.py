from Database import Database
from User import User

class UserState:
    user = None

    # Names of all movies the user has access
    movies_dict = None

    # Names of all movies the user has access to
    genres_dict = None

    # Object version of all_movies
    movie_map = None

    # Object version of all_genres
    genre_map = None

    # Contains all User states
    _map = {}

    def __init__(self, user):

       # tmpUser = Database.users.find_one({"user_key": user})
        self.user = user #User.build(tmpUser)
        self.movies_dict, self.genres_dict, self.movie_map, self.genre_map = Database.read_data(self.user.get_key())

        self.__class__._map[self.get_key()] = self

    def rebuild_maps(self):
        self.movies_dict, self.genres_dict, self.movie_map, self.genre_map = Database.read_data(self.user.get_key())

    def get_key(self):
        return self.user.get_key()

    @classmethod
    def lookup(cls, user_key):
        if user_key in cls._map:
            return cls._map[user_key]
        else:
            return None

    def lookup_genre(self, key):
        genre = next((genre for genre in self.genre_map if genre.name == key), None)

        return genre

    def lookup_movie(self, key):
        return next((movie for movie in self.movie_map if movie.title == key), None)


