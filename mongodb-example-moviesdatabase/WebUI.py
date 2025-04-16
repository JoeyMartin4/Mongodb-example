from Database import Database
import input_validation
import MovieGenre
import os
import configparser
from flask import Flask, render_template, request, redirect, url_for, session
from User import User
from UserState import UserState


class WebUI:
    user_state = None
    db = Database()
    app = Flask(__name__)
    app.secret_key = "841113210511010210511010511612132971101003298101121111110100"

    @staticmethod
    @app.before_request
    def require_login():
        allowed_routes = ['login', 'do_login', 'static']
        if request.endpoint not in allowed_routes and 'user' not in session:
            return redirect(url_for('login'))
        user_state = UserState.lookup(Database.get_user_key())
        if user_state is None:
            user_doc = Database.users.find_one({"username": Database.get_user()})
            if user_doc:
                user = User(Database.get_user(), user_doc["password_hash"])
                user_state = UserState(user)

    @staticmethod
    @app.route("/")
    def home():
        return render_template("index.html")

    @staticmethod
    @app.route("/categories")
    def categories():
        user_state = UserState.lookup(Database.get_user_key())
        genres = Database.read_user_genres(user_state.get_key())
        return render_template("categories.html", categories=genres)

    @classmethod
    def lookup_genre(cls, key):
        user_state = UserState.lookup(Database.get_user_key())
        if user_state is not None:
            return user_state.lookup_genre(key)

    @classmethod
    def lookup_movie(cls, key):
        user_state = UserState.lookup(Database.get_user_key())
        if user_state is not None:
            return user_state.lookup_movie(key)


    @staticmethod
    @app.route("/category_create")
    def category_create():
        user_state = UserState.lookup(Database.get_user_key())
        genres = Database.read_user_genres(user_state.get_key())
        return render_template("category_create.html", categories=genres)

    @staticmethod
    @app.route("/category_delete")
    def category_delete():
        user_state = UserState.lookup(Database.get_user_key())
        genres = Database.read_user_genres(user_state.get_key())
        return render_template("category_delete.html", categories=genres)

    @staticmethod
    @app.route("/movie_create")
    def movie_create():
        user_state = UserState.lookup(Database.get_user_key())
        movies = Database.read_user_movies(user_state.get_key())
        return render_template("movie_create.html", categories=movies)

    @staticmethod
    @app.route("/add_movie_to_category")
    def movie_to_category():
        user_state = UserState.lookup(Database.get_user_key())
        return render_template("add_movie_to_category.html",
                               movies=Database.read_user_movies(user_state.get_key()),
                               categories=Database.read_user_genres(user_state.get_key()))

    @staticmethod
    @app.route("/remove_movie_from_category")
    def remove_movie_from_category():
        user_state = UserState.lookup(Database.get_user_key())
        return render_template("remove_movie_from_category.html",
                               movies=Database.read_user_movies(user_state.get_key()),
                               categories=Database.read_user_genres(user_state.get_key()))

    @staticmethod
    @app.route("/update_movie_info")
    def update_movie_info():
        user_state = UserState.lookup(Database.get_user_key())
        return render_template("update_movie_info.html",
                               movies=Database.read_user_movies(user_state.get_key()))

    @staticmethod
    @app.route("/combine_categories")
    def combine_categories():
        user_state = UserState.lookup(Database.get_user_key())
        return render_template("combine_categories.html",
                               categories=Database.read_user_genres(user_state.get_key()))

    @staticmethod
    @app.route("/category/<category_name>")
    def category(category_name):
        user_state = UserState.lookup(Database.get_user_key())
        genre = user_state.lookup_genre(category_name)
        #genre = next((g for g in Database.read_user_genres() if g["name"] == category_name), None)
        if not genre:
            return render_template("error.html",
                                   message_header="Category not found",
                                   message_body="The category you're looking for cannot be found or is empty.",
                                   link="/categories",
                                   link_name="See categories"
                                   )
        movies = [user_state.lookup_movie(movie["title"]) for movie in genre.items]

       # movies = [Database.movies.find_one({"title": title}) for title in genre["movies"]]
        return render_template("category.html",
                               category_name=category_name,
                               movies=movies), WebUI.refresh_data()

    @staticmethod
    @app.errorhandler(404)
    def page_not_found(variable_name):
        return render_template(
            "error.html",
            message_header="Page not found",
            message_body="The page you're looking for cannot be found.",
            link="/",
            link_name="Back to home"
        )

    @staticmethod
    @app.route("/login", methods=["GET"])
    def login():
        return render_template("login.html")

    @staticmethod
    @app.route("/logout")
    def logout():
        session.pop("user", None)
        return redirect(url_for("login"))

    # Create actions
    @staticmethod
    @app.route('/do_create_category', methods=['GET', 'POST'])
    def do_create_category():
        user_state = UserState.lookup(Database.get_user_key())
        name = request.form["newname"]
        if name == "":
            return render_template(
                "error.html",
                message_header="Name not specified",
                message_body="There is no name for the category! Input one and try again.",
                link="category_create",
                link_name="Try again"
            )
        else:
            genre = next((g for g in Database.read_user_genres(user_state.get_key()) if g["name"] == name), None)
            if genre:
                return render_template("error.html",
                                       message_header="Category already exists",
                                       message_body="This category already exists! "
                                                    "Input a different one and try again.",
                                       link="category_create",
                                       link_name="Try again"
                                       )
            else:
                Database.add_genre(name)
                genres = Database.read_user_genres(user_state.get_key())
                return render_template("category_create.html", categories=genres), WebUI.refresh_data()

    @staticmethod
    @app.route('/do_create_movie', methods=['GET', 'POST'])
    def do_create_movie():
        user_key = Database.get_user_key()
        title = request.form["title"]
        if title == "":
            return render_template(
                "error.html",
                message_header="Title not specified",
                message_body="There is no title for this movie! Input one and try again.",
                link="movie_create",
                link_name="Try again"
            ), refresh_data()
        director = request.form["director"]
        if director == "":
            return render_template(
                "error.html",
                message_header="Director not specified",
                message_body="There is no director for this movie! Input one and try again.",
                link="movie_create",
                link_name="Try again"
            )
        year = request.form["year"]
        if year == "":
            return render_template(
                "error.html",
                message_header="Year not specified",
                message_body="There is no year for this movie! Input one and try again.",
                link="movie_create",
                link_name="Try again"
            )
        try:
            value = int(year)
        except ValueError:
            refresh_data()
            return render_template(
                "error.html",
                message_header="Year is not valid",
                message_body="Years are whole numbers! Input one and try again.",
                link="movie_create",
                link_name="Try again")
        Database.add_owned_movie(title, director, year, user_key)
        Database.add_movie_to_genre("All Movies", title, user_key)

        return render_template("movie_create.html"), WebUI.refresh_data()

    # Delete actions
    @staticmethod
    @app.route('/do_delete_category', methods=['GET', 'POST'])
    def do_delete_category():
        user_key = Database.get_user_key()
        name = request.form["deleting"]
        Database.delete_genre(name)
        genres = Database.read_user_genres(user_key)

        return render_template("category_delete.html", categories=genres), WebUI.refresh_data()

    # Miscellaneous Actions
    @staticmethod
    @app.route('/do_add_movie_to_category', methods=['GET', 'POST'])
    def do_add_movie_to_category():
        user_key = Database.get_user_key()
        movie_title = request.form["movieselected"]
        genre_name = request.form["categoryselected"]
        Database.add_movie_to_genre(genre_name, movie_title, user_key)

        return render_template("add_movie_to_category.html",
                               movies=Database.read_user_movies(user_key),
                               categories=Database.read_user_genres(user_key)), WebUI.refresh_data()

    @staticmethod
    @app.route('/do_remove_movie_from_category', methods=['GET', 'POST'])
    def do_remove_movie_from_category():
        user_key = Database.get_user_key()
        parts = request.form["removing"].split("|")
        movie_title = parts[1]
        genre_name = parts[0]
        Database.remove_movie_from_genre(genre_name, movie_title, user_key)

        return render_template("remove_movie_from_category.html",
                               movies=Database.read_user_movies(user_key),
                               categories=Database.read_user_genres(user_key)), WebUI.refresh_data()


    @staticmethod
    @app.route('/do_update_movie_info', methods=['GET', 'POST'])
    def do_update_movie_info():
        user_key = Database.get_user_key()
        user_state = UserState.lookup(user_key)
        new_title = request.form["updatedtitle"]
        if new_title == "":
            return render_template(
                "error.html",
                message_header="Title not specified",
                message_body="There is no title for this movie! Input one and try again.",
                link="update_movie_info",
                link_name="Try again"
            )
        new_director = request.form["updateddirector"]
        if new_director == "":
            return render_template(
                "error.html",
                message_header="Director not specified",
                message_body="There is no director for this movie! Input one and try again.",
                link="update_movie_info",
                link_name="Try again"
            )
        new_year = request.form["updatedyear"]
        if new_year == "":
            return render_template(
                "error.html",
                message_header="Year not specified",
                message_body="There is no year for this movie! Input one and try again.",
                link="update_movie_info",
                link_name="Try again"
            )
        try:
            value = int(new_year)
        except ValueError:
            return render_template(
                "error.html",
                message_header="Year is not valid",
                message_body="Years are whole numbers! Input one and try again.",
                link="update_movie_info",
                link_name="Try again")
        movie_title = request.form["movieselected"]

        Database.update_movie(movie_title,
                              {
                                  "title": new_title,
                                  "director": new_director,
                                  "year": new_year
                              }, user_key)
        genres = user_state.genre_map
        for genre in genres:
            for movie in genre.items:
                if movie["title"] == movie_title:
                    Database.remove_movie_from_genre(genre.name, movie_title, user_key)
                    Database.add_movie_to_genre(genre.name, new_title, user_key)

        return (render_template("update_movie_info.html", movies=Database.read_user_movies(user_key)),
                WebUI.refresh_data())


    @staticmethod
    @app.route('/do_combine_categories', methods=['GET', 'POST'])
    def do_combine_categories():
        user_key = Database.get_user_key()
        category1 = Database.genres.find_one({"name": request.form["sourcecategory"], "user_key": user_key})
        category2 = Database.genres.find_one({"name": request.form["targetcategory"], "user_key": user_key})

        if category1 == category2:
            return render_template(
                "error.html",
                message_header="Cannot combine categories",
                message_body="The categories you have selected are the same! Select two different ones and try again.",
                link="combine_categories",
                link_name="Try again"
            )

        for item in category1["movies"]:
            Database.add_movie_to_genre(category2["name"], user_key, item,)
            Database.remove_movie_from_genre(category1["name"], user_key, item)

        WebUI.refresh_data()
        return render_template("combine_categories.html",
                               categories=Database.read_user_genres(user_key))

    @staticmethod
    @app.route("/do_login", methods=['GET', 'POST'])
    def do_login():
        username = request.form.get("username")
        password = request.form.get("password")
        user_doc = Database.users.find_one({"username": username})
        if user_doc:
            user = User(username, user_doc["password_hash"])
            logged_in = user.verify(password)
            if not logged_in:
                return render_template("login.html", error="Invalid credentials")
            isUserLoggedIn = Database.login_user(user)
            user_state = UserState(user)
            return redirect(url_for("home"))

    @staticmethod
    def refresh_data():
        Database.reconnect()
        user_state = UserState.lookup(Database.get_user_key())
        user_state.rebuild_maps()

def run():
    home_dir = os.environ.get("USERPROFILE", os.environ.get("HOME"))
    config_dir = os.path.join(home_dir, "movie_manager")
    config_file = os.path.join(config_dir, "movie_manager.ini")
    config = configparser.ConfigParser()
    config.read(config_file)
    certfile = config.get("ssl", "certfile")
    keyfile = config.get("ssl", "keyfile")
    ssl_context = (os.path.join(config_dir, certfile), os.path.join(config_dir, keyfile))
    WebUI.app.run(port=8433, debug=True, ssl_context=ssl_context, use_reloader=False)


#if __name__ == "__main__":
 #   run()
