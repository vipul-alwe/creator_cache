from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    team_name = db.Column(db.String(200), nullable=False)
    ts = db.Column(db.String(200), nullable=False)

class CreatorBible(db.Model):
    __tablename__ = 'creator_bible'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    brand_name = db.Column(db.String(200), nullable=False)
    campaign_name = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    creator_name = db.Column(db.String(200), nullable=False)
    channel_link = db.Column(db.String(200), nullable=False)
    ucid = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    language = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    trend_type = db.Column(db.String(100), nullable=True)
    pct_13_17 = db.Column(db.Float, nullable=True)
    yt_gen_z_13_24 = db.Column(db.Float, nullable=True)
    rpr = db.Column(db.Float, nullable=True)
    last_cost = db.Column(db.Float, nullable=True)
    last_campaign = db.Column(db.String(200), nullable=True)
    contacts = db.Column(db.String(500), nullable=True)
    contact_number = db.Column(db.String(15), nullable=True)
    email_id = db.Column(db.String(200), nullable=True)
    median_views = db.Column(db.Integer, nullable=True)
    last_deliverables = db.Column(db.String(500), nullable=True)
    ig_link = db.Column(db.String(200), nullable=True)
    ig_subs = db.Column(db.Integer, nullable=True)
