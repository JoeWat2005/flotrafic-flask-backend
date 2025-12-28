from flask import Blueprint, request, jsonify
from website_manager.app.models import Client, Enquiry
from website_manager.app import db
from website_manager.app.ai import summarise_enquiry
from website_manager.app.email import send_email

api = Blueprint("api", __name__, url_prefix="/api")

@api.route("/enquiry/<site_id>", methods=["POST"])
def handle_enquiry(site_id):
    data = request.json

    client = Client.query.filter_by(site_id=site_id).first()
    if not client:
        return jsonify({"error": "Invalid site"}), 404

    summary = summarise_enquiry(data["message"])

    enquiry = Enquiry(
        site_id=site_id,
        name=data["name"],
        email=data["email"],
        message=data["message"],
        ai_summary=summary,
    )

    db.session.add(enquiry)
    db.session.commit()

    send_email(
        to=client.email,
        subject="New website enquiry",
        body=f"""
AI Summary:
{summary}

From: {data['name']} ({data['email']})

Message:
{data['message']}
"""
    )

    return jsonify({"success": True})
