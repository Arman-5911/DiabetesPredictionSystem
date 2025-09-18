from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pregnancies = db.Column(db.Float)
    glucose = db.Column(db.Float)
    bloodpressure = db.Column(db.Float)
    skinthickness = db.Column(db.Float)
    insulin = db.Column(db.Float)
    bmi = db.Column(db.Float)
    dpf = db.Column(db.Float)
    age = db.Column(db.Float)
    result = db.Column(db.String(20))
