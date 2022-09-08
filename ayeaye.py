# coding: utf-8
from config import Config

from flask import Flask, g, redirect, render_template, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import os
#vvv vscode complains bot console allows this import :S
import flask_sijax

#import required tables from database model
from database_scheme import FilmCinema, FilmDb, FilmKeylist, FilmScreening, FilmInsert, FilmFestival

from forms import LoginForm

app = Flask(__name__)
app.config.from_object(Config)

# the next line is necessary with cPanel deployment
application = app
path = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')
app.config['SIJAX_STATIC_PATH'] = '/home/noah/.local/lib/python3.8/site-packages/static/js/sijax/sijax.js'
app.config['SIJAX_JSON_URI'] = '/home/noah/.local/lib/python3.8/site-packages/static/js/sijax/json2.js'
flask_sijax.Sijax(app)

#DB Configuration is handeld in config.py
db = SQLAlchemy(app)

#################################
#ajax routes
# Functions registered with @flask_sijax.route can use Sijax

# / basically the landing page
# Calls films alphabetically

@flask_sijax.route(app, '/films')
def films():
    filmid=0
    film = FilmDb.query.filter(FilmDb.filmid==filmid).first()
    films = FilmDb.query.order_by(FilmDb.titel1.asc()).all()

    kinos = {}
    for kino in FilmCinema.query.filter(FilmCinema.festival==FilmFestival.query.first().type):
        kinos[kino.name] = kino.to_dict()

    film_insert = FilmInsert.query.filter(FilmInsert.filmid==filmid).first()
    film_screenings=''

    def load_kontrollblatt(obj_response, filmid):
        #maybe join on film insert and screnings to call all data?
        film = FilmDb.query.filter(FilmDb.filmid==filmid).first()
        film_insert = FilmInsert.query.filter(FilmInsert.filmid==filmid).first()

        film_screenings = []
        for film_screening in FilmScreening.query.filter(FilmScreening.film_id==filmid).order_by(FilmScreening.zeit.asc(), FilmScreening.subzeit.asc()):
            film_screenings.append(film_screening.to_dict())

        film_keys = {}
        if film.enc == 1 or film_insert.Enc == 1:
            for key in FilmKeylist.query.filter(FilmKeylist.UUID==film_insert.UUID):
                film_keys[key.Server] = key.to_dict()
        else:
            film_keys = []
        obj_response.call('load_kontrollblatt', [film.to_dict(), film_insert.to_dict(), film_screenings, kinos, film_keys])

    if g.sijax.is_sijax_request:
        # Sijax request detected - let Sijax handle it
        g.sijax.register_callback('load_kontrollblatt', load_kontrollblatt)
        return g.sijax.process_request()

    # Regular (non-Sijax request) - render the page template
    return render_template("table_view.html", title="Home",
        film=film, 
        films=films, 
        film_insert=film_insert, 
        film_screenings=film_screenings, 
        kinos=kinos)

# /screenings a list of all screenings
# sorted by time

@flask_sijax.route(app, '/screenings')
def screenings():
    film=""
    film_insert = ""

    kinos = {}
    for kino in FilmCinema.query.filter(FilmCinema.festival==FilmFestival.query.first().type):
        kinos[kino.name] = kino.to_dict()

    film_screenings = FilmScreening.query.join(FilmDb, FilmDb.filmid == FilmScreening.film_id)\
        .add_columns(
            FilmDb.titel1,
            FilmDb.filmid,
            FilmDb.min,
            FilmScreening.ingested,
            FilmScreening.getestet,
            FilmScreening.kino,
            FilmScreening.zeit,
            FilmScreening.subzeit
            )\
        .order_by(
            FilmScreening.zeit.asc(),
            FilmScreening.subzeit.asc(),
            FilmScreening.kino.asc()
            )\
        .all()

    def load_kontrollblatt(obj_response, filmid):
        #maybe join on film insert and screnings to call all data?
        film = FilmDb.query.filter(FilmDb.filmid==filmid).first()
        film_insert = FilmInsert.query.filter(FilmInsert.filmid==filmid).first()

        film_screenings = []
        film_screenings_raw = FilmScreening.query\
            .filter(FilmScreening.film_id==filmid)\
            .order_by(
                FilmScreening.zeit.asc(),
                FilmScreening.subzeit.asc(),
                FilmScreening.kino.asc()
            )

        for film_screening in film_screenings_raw:
            film_screenings.append(film_screening.to_dict())

        film_keys = {}
        if film.enc == 1 or film_insert.Enc == 1:
            for key in FilmKeylist.query.filter(FilmKeylist.UUID==film_insert.UUID):
                film_keys[key.Server] = key.to_dict()
        else:
            film_keys = []
        obj_response.call('load_kontrollblatt', [film.to_dict(), film_insert.to_dict(), film_screenings, kinos, film_keys])

    if g.sijax.is_sijax_request:
        # Sijax request detected - let Sijax handle it
        g.sijax.register_callback('load_kontrollblatt', load_kontrollblatt)
        return g.sijax.process_request()

    # Regular (non-Sijax request) - render the page template
    return render_template("screenings.html", title="Screenings",
        film=film, 
        film_insert=film_insert, 
        film_screenings=film_screenings, 
        kinos=kinos)

#################################
#static non-ajax routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        redirect(url_for('index'))
    return render_template("login.html", title='Sign In', form=form)

@app.route('/incoming', methods=['POST','GET'])
def incoming():
    dcps = []
    try:
        dcps_raw = FilmInsert.query.join(FilmDb, FilmDb.filmid == FilmInsert.filmid)\
        .add_columns(
            FilmDb.titel1,
            FilmInsert.Enc,
            FilmInsert.CPL,
            FilmInsert.Anzahl,
            FilmInsert.OV,
            FilmInsert.VFof,
            FilmInsert.Comment,
            FilmInsert.Verpackung,
            FilmInsert.NAS2,
            FilmInsert.SYNC,
            FilmInsert.SIZE,
            FilmInsert.DATE
            )\
        .order_by(FilmInsert.DATE.desc()).all()
        dcps = dcps_raw
    except Exception as e:
        print(e)

    return render_template("incoming.html", title="Incoming", dcps=dcps)
  
@app.route('/index')
def index():
    return render_template("index.html")
    
##############################
# Main Loop of program
if __name__ == '__main__':
    app.run(debug=True, threaded=False)

