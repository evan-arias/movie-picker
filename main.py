from flask import Flask, request, render_template, session, redirect, url_for
import random
import json
import os
from datetime import datetime

# File to store movie lists
FILE_NAME = "movies.json"

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "your_secret_key"  # Needed for sessions

def load_movies():
    """Load movies from a JSON file."""
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {"Yas": [], "Evan": []}
    return {"Yas": [], "Evan": []}

def save_movies(movie_data):
    """Save movies to a JSON file."""
    with open(FILE_NAME, "w") as file:
        json.dump(movie_data, file, indent=4)

def get_seasonal_theme():
    """Determine the current seasonal theme."""
    today = datetime.now()
    if today.month == 2 and today.day == 14:
        return "valentine"  # Valentine's Day
    elif today.month == 10:
        return "halloween"  # Halloween (entire October)
    elif today.month == 12:
        return "christmas"  # Christmas (entire December)
    else:
        return "default"  # Default theme

@app.route("/", methods=["GET", "POST"])
def home():
    """Home page with seasonal theme."""
    message = ""
    theme = get_seasonal_theme()

    if request.method == "POST":
        name = request.form.get("name", "Yas")  # Default to "Yas"
        movie = request.form.get("movie")
        keyword = request.form.get("keyword")

        # Store the name in session if provided
        session["name"] = name

        movie_data = load_movies()
        user_name = session.get("name", "Yas")  # Default to "Yas"

        if keyword == "XXX":
            # Clear movie list
            movie_data = {"Yas": [], "Evan": []}
            save_movies(movie_data)
            message = "JOB COMPLETE!"
        elif user_name in movie_data and movie:
            # Add a movie using the name in session
            movie_data[user_name].append(movie)
            save_movies(movie_data)
            message = "Movie Added!"

    return render_template("index.html", message=message, theme=theme, name=session.get("name"))

@app.route("/random")
def pick_random_movie():
    """Pick a random movie from the combined list."""
    movie_data = load_movies()
    combined_movies = movie_data["Yas"] + movie_data["Evan"]
    if combined_movies:
        chosen_movie = random.choice(combined_movies)
        return render_template("random.html", chosen_movie=chosen_movie, theme=get_seasonal_theme())
    return render_template("random.html", chosen_movie="No movies in the list yet!", theme=get_seasonal_theme())

@app.route("/show")
def show_list():
    """Show the list of all movies."""
    movie_data = load_movies()
    return render_template(
        "index.html",
        yas_movies=movie_data["Yas"],
        evan_movies=movie_data["Evan"],
        theme=get_seasonal_theme(),
        name=session.get("name")
    )

if __name__ == "__main__":
    app.run(debug=True)
