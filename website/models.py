from datetime import timezone
from enum import unique

from matplotlib.pyplot import title
from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10000))
    author = db.Column(db.String(10000))
    date = db.Column(db.String(10000))
    filename = db.Column(db.Text, nullable=False)


