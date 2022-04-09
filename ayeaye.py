# coding: utf-8

from flask import Flask, g, render_template
from flask_sqlalchemy import SQLAlchemy
import os, json
#vvv vscode complains bot console allows this import :S
import flask_sijax

#import required tables from database model
from database_scheme import FilmCinema, FilmDb, FilmKeylist, FilmScreening, FilmInsert

app = Flask(__name__)
# the next line is necessary with cPanel deployment
application = app
path = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')
app.config['SIJAX_STATIC_PATH'] = '/home/noah/.local/lib/python3.8/site-packages/static/js/sijax/sijax.js'
app.config['SIJAX_JSON_URI'] = '/home/noah/.local/lib/python3.8/site-packages/static/js/sijax/json2.js'
flask_sijax.Sijax(app)

# make sure the username, password and database name are correct
username = 'drupal'
password = 'u%23nfC63Hu8R8r7yk'
userpass = 'mysql+pymysql://' + username + ':' + password + '@'
# keep this as is for a hosted website
server  = '37.252.189.147'
# change to YOUR database name, with a slash added as shown
dbname   = '/drupal_testing'
# put them all together as a string that shows SQLAlchemy where the database is
app.config['SQLALCHEMY_DATABASE_URI'] = userpass + server + dbname
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)


#################################
#ajax routes
# Functions registered with @flask_sijax.route can use Sijax

# / basically the landing page
# Calls films alphabetically

@flask_sijax.route(app, '/')
def inspection():
    filmid=0
    film = FilmDb.query.filter(FilmDb.filmid==filmid).first()
    films = FilmDb.query.order_by(FilmDb.titel1.asc()).all()

    kinos_raw = FilmCinema.query.filter(FilmCinema.festival=='D')
    kinos = []
    for kino in kinos_raw:
        kinos.append(kino.to_dict())

    film_insert = FilmInsert.query.filter(FilmInsert.filmid==filmid).first()
    film_screenings=''

    def load_kontrollblatt(obj_response, filmid):
        #maybe join on film insert and screnings to call all data?
        film = FilmDb.query.filter(FilmDb.filmid==filmid).first()
        film_insert = FilmInsert.query.filter(FilmInsert.filmid==filmid).first()

        film_screenings = []
        for film_screening in FilmScreening.query.filter(FilmScreening.film_id==filmid).order_by(FilmScreening.zeit.asc(), FilmScreening.subzeit.asc()):
            film_screenings.append(film_screening.to_dict())

        if film.enc == 1 or film_insert.Enc == 1:
            film_keys = FilmKeylist.query.filter(FilmKeylist.UUID==film_insert.UUID)
        else:
            film_keys = ''
        obj_response.call('load_kontrollblatt', [film.to_dict(), film_insert.to_dict(), film_screenings, kinos])

    if g.sijax.is_sijax_request:
        # Sijax request detected - let Sijax handle it
        g.sijax.register_callback('load_kontrollblatt', load_kontrollblatt)
        return g.sijax.process_request()

    # Regular (non-Sijax request) - render the page template
    return render_template("home.html", film=film, films=films, film_insert=film_insert, film_screenings=film_screenings, kinos=kinos)

# /screenings a list of all screenings
# sorted by time

@flask_sijax.route(app, '/screenings')
def screenings():
    film=""
    film_insert = ""
    kinos = []

    kinos_raw = FilmCinema.query.filter(FilmCinema.festival=='D')
    for kino in kinos_raw:
        kinos.append(kino.to_dict())

    film_screenings = FilmScreening.query.join(FilmDb, FilmDb.filmid == FilmScreening.film_id)\
        .add_columns(
            FilmDb.titel1,
            FilmDb.filmid,
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

        film_insert = FilmInsert.query.filter(FilmInsert.filmid==filmid).first()
        if film.enc == 1 or film_insert.Enc == 1:
            film_keys = FilmKeylist.query.filter(FilmKeylist.UUID==film_insert.UUID)
        else:
            film_keys = ''
        obj_response.call('load_kontrollblatt', [film.to_dict(), film_insert.to_dict(), film_screenings, kinos])

    if g.sijax.is_sijax_request:
        # Sijax request detected - let Sijax handle it
        g.sijax.register_callback('load_kontrollblatt', load_kontrollblatt)
        return g.sijax.process_request()

    # Regular (non-Sijax request) - render the page template
    return render_template("screenings.html", film=film, film_insert=film_insert, film_screenings=film_screenings, kinos=kinos)

#################################
#static non-ajax routes
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

    return render_template("incoming.html", dcps=dcps)
@app.route('/film/<filmid>', methods=['POST','GET'])
def film_einzeln(filmid):
    #maybe join on film insert and screnings to call all data?
    film = FilmDb.query.filter(FilmDb.filmid==filmid).first()
    film_screenings = FilmScreening.query.filter(FilmScreening.film_id==filmid)
    film_insert = FilmInsert.query.filter(FilmInsert.filmid==filmid).first()
    if film.enc == 1 or film_insert.Enc == 1:
        film_keys = FilmKeylist.query.filter(FilmKeylist.UUID==film_insert.UUID)
    else:
        film_keys = ''

    return render_template("film.html", film=film, film_insert=film_insert, film_screenings=film_screenings)
    
@app.route('/<filmid>')
def home(filmid=0):
    films = ''
    #maybe join on film insert and screnings to call all data?
    film = FilmDb.query.filter(FilmDb.filmid==filmid).first()
    film_screenings = FilmScreening.query.filter(FilmScreening.film_id==filmid)
    film_insert = FilmInsert.query.filter(FilmInsert.filmid==filmid).first()
    if film.enc == 1 or film_insert.Enc == 1:
        film_keys = FilmKeylist.query.filter(FilmKeylist.UUID==film_insert.UUID)
    else:
        film_keys = '' 

    try:
        films = FilmDb.query.order_by(FilmDb.titel1.asc()).all()
    except Exception as e:
        # see Terminal for description of the error
        print(e)

    return render_template("home.html", film=film, films=films, film_insert=film_insert, film_screenings=film_screenings)
    
##############################
# Main Loop of program
if __name__ == '__main__':
    app.run(debug=True)

