from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
from dotenv import load_dotenv
import os

load_dotenv()

access_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxZjY5MTRmZjhjZTY3NDAxYzk1YzJkMGNmNjc3NDM4MyIsInN1YiI6IjY1NWI0OTczZDRmZTA0MDBhYzM4ZjFiMyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.zhNvu3vcQ2aHGQSQ-o7pp90ilRaxPQevaytKOMQx_Ng"

url = "https://api.themoviedb.org/3/search/movie"

header = {
    "accept": "application/json",
    "Authorization": f"Bearer {access_token}"
}


api_key = os.environ.get('API_KEY')
'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///top_movies-collection.db"
Bootstrap5(app)


db = SQLAlchemy()

db.init_app(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    image_url = db.Column(db.String, nullable=False)


# with app.app_context():
#     db.create_all()


# with app.app_context():
#     first_movie = Movie(
#         # id=1,
#         title="Phone Booth",
#         year=2002,
#         description="Publicist Staurt Shepard finds himself trapped in a phone booth, pinned down by an extortionist's"
#                     "rifle. Unable to leave or receive outside help, Staurt's negotiation with the caller leads to jaw-"
#                     "dropping climax.",
#         rating=7.3,
#         ranking=10,
#         review="My favourite character was the caller.",
#         image_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
#                 'https://image.tmdb.org/t/p/w500/8c4a8kE7PizaGQQnditMmI1xbRp.jpg'
#     )
#     db.session.add(first_movie)
#     db.session.commit()

# with app.app_context():
#     second_movie = Movie(
#         title="Avatar The Way of Water",
#         year=2022,
#         description="Set more than a decade after the events of the first film, learn the story of the Sully family"
#                     " (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each"
#                     " other safe, the battles they fight to stay alive, and the tragedies they endure.",
#         rating=7.3,
#         ranking=9,
#         review="I liked the water.",
#         image_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
#     )
#     db.session.add(second_movie)
#     db.session.commit()


@app.route("/")
def home():
    # result = db.session.execute(db.select(Movie))
    result = db.session.query(Movie).order_by(Movie.rating)
    all_movies = result.all()  # convert ScalarResult to Python List

    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()

    return render_template("index.html", movies=all_movies)


class Edit(FlaskForm):
    rating = StringField(label="Your rating out of 10 e.g: 7.5", validators=[DataRequired()])
    review = StringField(label="Your review", validators=[DataRequired()])
    submit = SubmitField(label="Done")


@app.route("/edit", methods=["POST", "GET"])
def edit_rating_review():
    form = Edit()
    movie_id = request.args.get("id")
    movie = db.get_or_404(Movie, movie_id)
    if request.method == "POST":
        movie.rating = request.form["rating"]
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", edit=form, movie=movie)


@app.route("/delete")
def delete_card():
    movie_id = request.args.get("id")
    movie = db.get_or_404(Movie, movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home"))


class AddMovie(FlaskForm):
    add = StringField(label="Movie Title", validators=[DataRequired()])
    submit = SubmitField(label="Add Movie")


@app.route("/add", methods=["GET", "POST"])
def add_movie():
    addmovie = AddMovie()
    if request.method == "POST":
        movie_title = request.form["add"]
        parameter = {
            "api_key": api_key,
            "query": movie_title,
        }
        response = requests.get(url=url, params=parameter)
        data = response.json()["results"]
        return render_template("select.html", options=data)
    return render_template("add.html", addmovie=addmovie)


@app.route("/find")
def find_movie():
    movie_id = request.args.get("id")
    movie_id_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    parameter = {
        "api_key": api_key,
        "language": "en-US"
    }
    if movie_id_url:
        response = requests.get(url=movie_id_url, params=parameter)
        data = response.json()
        image_url_first_half = "https://image.tmdb.org/t/p/w500"
        movie = Movie(
            title=data["original_title"],
            year=data["release_date"].split("-")[0],
            description=data["overview"],
            image_url=f"{image_url_first_half}{data['poster_path']}"
        )
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)
