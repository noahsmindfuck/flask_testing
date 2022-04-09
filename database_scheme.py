# coding: utf-8
from sqlalchemy import Column, DateTime, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT, VARCHAR
from flask_sqlalchemy import SQLAlchemy

#required for .to_dict() JSON serializing
#extend Classes from SerializerMixin
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class FilmCinema(db.Model, SerializerMixin):
    __tablename__ = 'film_cinemas'

    ID = Column(INTEGER(3), primary_key=True)
    name = Column(String(5), nullable=False)
    name_long = Column(String(64), nullable=False)
    festival = Column(String(1), nullable=False)
    Servernummer = Column(String(9), nullable=False, comment='dedicated server number for cinema')


class FilmDb(db.Model, SerializerMixin):
    __tablename__ = 'film_db'

    filmid = Column(INTEGER(10), primary_key=True, unique=True)
    medium = Column(String(10), nullable=False)
    schiene = Column(String(10))
    enc = Column(INTEGER(1))
    artikel = Column(String(10))
    titel1 = Column(String(254))
    titel2 = Column(String(254))
    regie = Column(String(254))
    land = Column(String(100))
    min = Column(INTEGER(3))
    jahr = Column(String(10))
    dcpname = Column(String(255))
    dcpsize = Column(String(10))
    presetDB = Column(String(10))
    preset = Column(String(10))
    kasch = Column(String(10))
    bildformat = Column(String(10))
    tonformat = Column(String(10))
    toninfo = Column(String(10))
    tonsystem = Column(String(10))
    fps = Column(String(10))
    playlist = Column(String(255))
    dcp_start = Column(String(10))
    ersterTONnach = Column(String(10))
    ersterUTnach = Column(String(10))
    sprache = Column(String(100))
    untertitel = Column(String(100))
    ut_art = Column(String(10))
    fassung = Column(String(18))
    letzterTitel = Column(String(255))
    kontrolle = Column(String(10))
    hinweise_rot = Column(String(255))
    hinweise_von_projektion = Column(String(255))
    datenbank = Column(String(933))
    archiv = Column(TINYINT(1))
    koppelverbot = Column(TINYINT(1))
    sichtungslink = Column(String(255), nullable=False)
    sichtungspasswort = Column(String(255), nullable=False)
    last_edit_by = Column(String(10), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    #screenings = db.relationship('FilmScreening', backref='screenings', lazy='dynamic')

class FilmDbChangelog(db.Model):
    __tablename__ = 'film_db_changelog'

    index_changelog = Column(String(100), primary_key=True, index=True)
    filmid = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
    schiene = Column(String(10))
    enc = Column(String(1))
    artikel = Column(String(10))
    titel1 = Column(String(254), index=True)
    regie = Column(String(254))
    min = Column(INTEGER(3))
    jahr = Column(String(10))
    land = Column(String(100))
    dcpname = Column(String(255))
    dcpsize = Column(String(10))
    presetDB = Column(String(10))
    preset = Column(String(10))
    kasch = Column(String(10))
    tonformat = Column(String(10))
    toninfo = Column(String(10))
    fps = Column(String(10))
    playlist = Column(String(255))
    dcp_start = Column(String(10))
    ersterTONnach = Column(String(10))
    ersterUTnach = Column(String(10))
    sprache = Column(String(100))
    untertitel = Column(String(100))
    ut_art = Column(String(10))
    fassung = Column(String(45))
    letzterTitel = Column(String(255))
    kontrolle = Column(String(10))
    hinweise_rot = Column(String(255))
    hinweise_von_projektion = Column(String(255))
    datenbank = Column(String(255))
    last_edit_by = Column(String(20), nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False, index=True, server_default=text("CURRENT_TIMESTAMP"))


class FilmDbOriginal(db.Model):
    __tablename__ = 'film_db_original'

    filmid = Column(INTEGER(10), primary_key=True, unique=True)
    medium = Column(String(10), nullable=False)
    schiene = Column(String(10))
    enc = Column(INTEGER(1))
    artikel = Column(String(10))
    titel1 = Column(String(254))
    titel2 = Column(String(254))
    regie = Column(String(254))
    land = Column(String(100))
    min = Column(INTEGER(3))
    jahr = Column(String(10))
    dcpname = Column(String(255))
    dcpsize = Column(String(10))
    presetDB = Column(String(10))
    preset = Column(String(10))
    kasch = Column(String(10))
    bildformat = Column(String(10))
    tonformat = Column(String(10))
    toninfo = Column(String(10))
    tonsystem = Column(String(10))
    fps = Column(String(10))
    playlist = Column(String(255))
    dcp_start = Column(String(10))
    ersterTONnach = Column(String(10))
    ersterUTnach = Column(String(10))
    sprache = Column(String(100))
    untertitel = Column(String(100))
    ut_art = Column(String(10))
    fassung = Column(String(18))
    letzterTitel = Column(String(255))
    kontrolle = Column(String(10))
    hinweise_rot = Column(String(255))
    hinweise_von_projektion = Column(String(255))
    datenbank = Column(String(933))
    archiv = Column(TINYINT(1))
    koppelverbot = Column(TINYINT(1))
    last_edit_by = Column(String(10), nullable=False)
    timestamp = Column(DateTime, nullable=False)


class FilmFestival(db.Model):
    __tablename__ = 'film_festival'

    type = Column(String(5), primary_key=True, server_default=text("''"), comment='here the festival is specified')


class FilmIdKonventionen(db.Model):
    __tablename__ = 'film_id_konventionen'

    Prefix = Column(INTEGER(1), nullable=False)
    Bedeutung = Column(String(255), nullable=False)
    ID = Column(INTEGER(11), primary_key=True)


class FilmInsert(db.Model, SerializerMixin):
    __tablename__ = 'film_insert'

    ID = Column(INTEGER(11), primary_key=True)
    filmid = Column(INTEGER(5), nullable=False)
    CPL = Column(String(255, 'utf8_bin'), nullable=False, unique=True)
    Verpackung = Column(String(255, 'utf8_bin'))
    Container = Column(String(255, 'utf8_bin'))
    Anzahl = Column(String(3, 'utf8_bin'), nullable=False, server_default=text("'0'"))
    OV = Column(INTEGER(1), nullable=False, server_default=text("'0'"), comment='Set to 1 if CPL is OV')
    VFof = Column(INTEGER(10), nullable=False, server_default=text("'0'"), comment='defines OV for VF')
    Enc = Column(INTEGER(1), nullable=False, server_default=text("'0'"), comment='0 = not encrypted')
    Zubehoer = Column(String(255, 'utf8_bin'))
    Comment = Column(String(1024, 'utf8_bin'))
    UUID = Column(String(255, 'utf8_bin'), nullable=False, server_default=text("'-'"))
    NAS2 = Column(String(5, 'utf8_bin'), comment='U = upload, F = Fertig')
    SYNC = Column(String(1, 'utf8_bin'), nullable=False, server_default=text("'0'"), comment='0=no,1=yes')
    SIZE = Column(String(6, 'utf8_bin'), nullable=False, comment='in GB')
    PATH = Column(String(255, 'utf8_bin'))
    root = Column(String(255, 'utf8_bin'))
    inspect_log = Column(Text(collation='utf8_bin'), nullable=False)
    inspect_errors = Column(INTEGER(10), nullable=False)
    DATE = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))


class FilmKeylist(db.Model, SerializerMixin):
    __tablename__ = 'film_keylist'

    key_id = Column(INTEGER(5), primary_key=True, unique=True)
    Titel = Column(Text)
    Server = Column(Text)
    Valid_From = Column(Text)
    Valid_Till = Column(Text)
    UUID = Column(Text)
    Last_Modified = Column(Text)


class FilmScreening(db.Model, SerializerMixin):
    __tablename__ = 'film_screenings'

    screening_id = Column(INTEGER(6), primary_key=True, unique=True, server_default=text("'0'"))
    film_id = Column(INTEGER(6))
    #film_id = Column(INTEGER(6), db.ForeignKey('FilmDb.filmid'))
    kino = Column(String(2))
    zeit = Column(DateTime, nullable=False)
    subzeit = Column(DateTime, nullable=False)
    soundsetting = Column(String(10))
    fassung = Column(String(18))
    ingested = Column(INTEGER(1))
    getestet = Column(INTEGER(1))
    kdm_vonbis = Column(String(10))
    last_edit_by = Column(String(10))
    timestamp = Column(DateTime)

class FilmScreeningsChangelog(db.Model):
    __tablename__ = 'film_screenings_changelog'

    index_changelog = Column(VARCHAR(100), primary_key=True)
    screening_id = Column(VARCHAR(10), index=True)
    film_id = Column(INTEGER(6), index=True)
    kino = Column(VARCHAR(30))
    subzeit = Column(DateTime)
    zeit = Column(DateTime)
    soundsetting = Column(VARCHAR(10))
    ingested = Column(TINYINT(1), server_default=text("'0'"))
    getestet = Column(TINYINT(1), server_default=text("'0'"))
    kdm_vonbis = Column(VARCHAR(20))
    last_edit_by = Column(VARCHAR(20), nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class FilmScreeningsOriginal(db.Model):
    __tablename__ = 'film_screenings_original'

    screening_id = Column(INTEGER(6), primary_key=True, server_default=text("'0'"))
    film_id = Column(INTEGER(5))
    kino = Column(String(2))
    zeit = Column(String(12))
    subzeit = Column(String(12))
    soundsetting = Column(String(10), nullable=False)
    fassung = Column(String(18))
    ingested = Column(String(10))
    getestet = Column(String(10))
    kdm_vonbis = Column(String(10))
    last_edit_by = Column(String(10))
    timestamp = Column(String(10))


class FilmServer(db.Model):
    __tablename__ = 'film_server'

    Seriennummer = Column(String(100), primary_key=True, unique=True)
    Ort = Column(String(100), nullable=False)
    Firma = Column(String(50), nullable=False)
    Art = Column(String(100), nullable=False)
    fix = Column(TINYINT(4), nullable=False)
    Kommentar = Column(String(100), nullable=False)

class FilmUser(db.Model):
    __tablename__ = 'film_user'
    
    id = Column(INTEGER, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
