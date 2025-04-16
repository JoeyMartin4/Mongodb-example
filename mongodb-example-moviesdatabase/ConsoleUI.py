"""
A console-based user interface to manage movies and categories.

This module uses the input_validation functions for robust user input.
"""

import input_validation
from Movie import Movie
from OwnedMovie import OwnedMovie
from MovieGenre import MovieGenre
from read_database import load_movies, load_owned_movies, load_categories

class ConsoleUI:
    def __init__(self):
        """Initialize the UI with data from the database."""
        self.all_items = MovieGenre("All Movies")
        self.categories = load_categories()

        # Load movies into "All Movies"
        for movie in load_movies() + load_owned_movies():
            self.all_items.add(movie)


    def show_menu(self):
        """
        Display the main menu options.
        """
        print("\n1. Show all categories") #done
        print("2. Create new category")
        print("3. Delete category")
        print("4. Show items in category") # done
        print("5. Create new item")
        print("6. Add item to category")
        print("7. Remove item from category")
        print("8. Update item information")
        print("9. Combine categories")
        print("10. Exit")

    def run(self):
        """
        Run the main loop for the console UI.
        """
        while True:
            self.show_menu()
            choice = input_validation.input_value(
                "int", prompt="Enter your choice: ", ge=1, le=10
            )
            if choice == 1:
                self.show_categories()
            elif choice == 2:
                self.create_category()
            elif choice == 3:
                self.delete_category()
            elif choice == 4:
                self.show_items_in_category()
            elif choice == 5:
                self.create_item()
            elif choice == 6:
                self.add_item_to_category()
            elif choice == 7:
                self.remove_item_from_category()
            elif choice == 8:
                self.update_item()
            elif choice == 9:
                self.combine_categories()
            elif choice == 10:
                print("Exiting...")
                break

    def show_categories(self):
        """
        Display all available categories.
        """
        for category in self.categories:
            print(category)

    def create_category(self):
        """
        Create a new movie category.
        """
        name = input_validation.input_value(
            "string", prompt="Enter category name: "
        )
        category = MovieGenre(name)
        self.categories.append(category)

    def delete_category(self):
        """
        Delete a movie category.
        """
        name = input_validation.input_value(
            "string", prompt="Enter category name to delete: "
        )
        for category in self.categories:
            if category.name == name:
                self.categories.remove(category)
                break

    def show_items_in_category(self):
        """
        Show all movies in a specified category.
        """
        name = input_validation.input_value(
            "string", prompt="Enter category name to show items: "
        )
        for category in self.categories:
            if category.name == name:
                for item in category:
                    print(item)
                break

    def create_item(self):
        """
        Create a new Movie or OwnedMovie item.
        """
        print("1. Create a Movie")
        print("2. Create an Owned Movie")
        choice = input_validation.input_value(
            "int", prompt="Choose item type: ", ge=1, le=2
        )

        title = input_validation.input_value(
            "string", prompt="Enter title: "
        )
        director = input_validation.input_value(
            "string", prompt="Enter director: "
        )
        release_year = input_validation.input_value(
            "int", prompt="Enter release year: ", ge=1880
        )

        if choice == 1:
            item = Movie(title, director, release_year)
        elif choice == 2:
            series_name = input_validation.input_value(
                "string", prompt="Enter series name: "
            )
            item = OwnedMovie(title, director, release_year, series_name)

        self.all_items.add(item)
        print(f"Item created: {item}")

    def add_item_to_category(self):
        """
        Add an existing item to a movie category.
        """
        item_title = input_validation.input_value(
            "string", prompt="Enter item title to add to category: "
        )
        category_name = input_validation.input_value(
            "string", prompt="Enter category name: "
        )
        for category in self.categories:
            if category.name == category_name:
                for item in self.all_items:
                    if (item.title == item_title and
                            item not in category):
                        category.add(item)
                        print(f"Item {item_title} added to "
                              f"category {category_name}")
                        break

    def remove_item_from_category(self):
        """
        Remove an item from a movie category.
        """
        item_title = input_validation.input_value(
            "string", prompt="Enter item title to remove from category: "
        )
        category_name = input_validation.input_value(
            "string", prompt="Enter category name: "
        )
        for category in self.categories:
            if category.name == category_name:
                for item in category:
                    if item.title == item_title:
                        category.remove(item)
                        print(f"Item {item_title} removed from "
                              f"category {category_name}")
                        break

    def update_item(self):
        """
        Update the information of an existing item.
        """
        item_title = input_validation.input_value(
            "string", prompt="Enter item title to update: "
        )
        for item in self.all_items:
            if item.title == item_title:
                title = input_validation.input_value(
                    "string", prompt=f"Enter new title (current: "
                                     f"{item.title}): "
                )
                director = input_validation.input_value(
                    "string", prompt=f"Enter new director (current: "
                                     f"{item.director}): "
                )
                release_year = input_validation.input_value(
                    "int", prompt=f"Enter new release year (current: "
                                  f"{item.release_year}): ", ge=1880
                )
                if hasattr(item, "series_name"):
                    series_name = input_validation.input_value(
                        "string", prompt=f"Enter new series name (current: "
                                         f"{item.series_name}): "
                    )
                    item.update(title, director, release_year,
                                series_name=series_name)
                else:
                    item.update(title, director, release_year)
                print(f"Item updated: {item}")

    def combine_categories(self):
        """
        Combine two categories into a new category.
        """
        cat_name1 = input_validation.input_value(
            "string", prompt="Enter first category name: "
        )
        cat_name2 = input_validation.input_value(
            "string", prompt="Enter second category name: "
        )

        cat1 = None
        cat2 = None
        for category in self.categories:
            if category.name == cat_name1:
                cat1 = category
            elif category.name == cat_name2:
                cat2 = category

        if cat1 and cat2:
            new_category = cat1 + cat2
            self.categories.append(new_category)
            print(f"New combined category: {new_category}")


if __name__ == "__main__":
    ui = ConsoleUI()
    ui.run()
