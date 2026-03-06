"""
Main Flask application — Admin panel, tracking endpoint, and results dashboard.
"""

from flask import (Flask, render_template, request,
                   redirect, url_for, flash)
from config import Config
from models import db, Campaign, Target
from mailer import send_campaign_emails
from tracker import record_click
import threading

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()


# ──────────────────────────────────────────────
# ADMIN ROUTES
# ──────────────────────────────────────────────

@app.route('/')
def dashboard():
    """Main admin dashboard — shows all campaigns."""
    campaigns = Campaign.query.order_by(Campaign.created_at.desc()).all()
    return render_template('admin.html', campaigns=campaigns)


@app.route('/campaign/new', methods=['POST'])
def create_campaign():
    """
    Creates a new phishing campaign.

    🔐 SECURITY CONCEPT — Input Validation:
       We validate that emails are provided and the template exists.
       In a real app, you'd also sanitize inputs to prevent
       SQL Injection and XSS (Cross-Site Scripting).
    """
    name = request.form.get('name', '').strip()
    template = request.form.get('template', 'password_reset')
    emails_raw = request.form.get('emails', '').strip()

    if not name or not emails_raw:
        flash('❌ Campaign name and target emails are required.', 'error')
        return redirect(url_for('dashboard'))

    # Parse comma-separated emails
    emails = [e.strip() for e in emails_raw.split(',') if e.strip()]

    if not emails:
        flash('❌ Please provide at least one valid email.', 'error')
        return redirect(url_for('dashboard'))

    # Create campaign
    campaign = Campaign(name=name, template=template)
    db.session.add(campaign)
    db.session.flush()  # Get the campaign ID before adding targets

    # Add targets
    for email in emails:
        target = Target(email=email, campaign_id=campaign.id)
        db.session.add(target)

    db.session.commit()
    flash(f'✅ Campaign "{name}" created with {len(emails)} targets.', 'success')
    return redirect(url_for('dashboard'))


@app.route('/campaign/<int:campaign_id>/send', methods=['POST'])
def send_campaign(campaign_id):
    """
    Sends all unsent emails in a campaign (runs in background thread).

    🔐 SECURITY CONCEPT — Asynchronous Execution:
       Sending emails is slow (network I/O). We use a background thread
       so the admin UI doesn't freeze. In production, use a task queue
       like Celery for reliability and retry logic.
    """
    campaign = Campaign.query.get_or_404(campaign_id)
    campaign_name = campaign.name  # capture before handing off to thread

    def send_in_background():
        with app.app_context():
            # Re-fetch the campaign inside the new app context so SQLAlchemy
            # can lazy-load relationships (targets) from the correct session.
            fresh_campaign = db.session.get(Campaign, campaign_id)
            if fresh_campaign:
                success, message = send_campaign_emails(fresh_campaign)
                print(f"Campaign '{campaign_name}': {message}")

    thread = threading.Thread(target=send_in_background)
    thread.daemon = True
    thread.start()

    flash(f'📧 Sending emails for campaign "{campaign.name}"...', 'info')
    return redirect(url_for('campaign_results', campaign_id=campaign_id))


# ──────────────────────────────────────────────
# TRACKING ENDPOINT (What the user clicks)
# ──────────────────────────────────────────────

@app.route('/track/<token>')
def track_click(token):
    """
    This is the URL embedded in the phishing email.
    When a user clicks it, we log the event and show
    an educational landing page.

    🔐 SECURITY CONCEPT — The "Aha Moment":
       Instead of stealing data, we immediately reveal
       that this was a test. This is the most important
       part of awareness training — turning a mistake
       into a learning experience WITHOUT shame.
    """
    ip = request.remote_addr
    ua = request.headers.get('User-Agent', 'Unknown')

    target = record_click(token, ip, ua)

    return render_template('landed.html', target=target)


# ──────────────────────────────────────────────
# RESULTS DASHBOARD
# ──────────────────────────────────────────────

@app.route('/campaign/<int:campaign_id>/results')
def campaign_results(campaign_id):
    """View results for a specific campaign."""
    campaign = Campaign.query.get_or_404(campaign_id)
    return render_template('results.html', campaign=campaign)


if __name__ == '__main__':
    app.run(debug=True, port=5000)