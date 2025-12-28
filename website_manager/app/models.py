from website_manager.app import db
from datetime import datetime

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    site_id = db.Column(db.String(50), unique=True)

class Enquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.String(50))
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    message = db.Column(db.Text)
    ai_summary = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
