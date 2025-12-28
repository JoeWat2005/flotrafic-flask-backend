from flask import Blueprint, render_template
from website_manager.app.models import Enquiry

admin = Blueprint("admin", __name__, url_prefix="/admin")

@admin.route("/")
def dashboard():
    enquiries = Enquiry.query.order_by(Enquiry.created_at.desc()).all()
    return render_template("admin.html", enquiries=enquiries)
