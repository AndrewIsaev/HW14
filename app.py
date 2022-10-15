from flask import Flask

import utils

# Create app
app = Flask(__name__)
app.config["DEBUG"]=True

# Create views search_by_title
@app.route('/movie/<title>')
def search_by_title(title):  # put application's code here
    return utils.search_movie_by_title(title)

# Create views search_between_year
@app.route('/movie/<int:start_year>/to/<int:stop_year>')
def search_between_years(start_year, stop_year):
    return utils.search_between_years(start_year, stop_year)

# Create views search_by_rating
@app.route('/rating/<rating>')
def search_by_rating(rating):
    return utils.search_by_rating(rating)

# Create views last_ten_films_by_genre
@app.route('/genre/<genre>')
def last_ten_films_by_genre(genre):
    return utils.get_last_ten_films_by_genre(genre)


if __name__ == '__main__':
    app.run()
