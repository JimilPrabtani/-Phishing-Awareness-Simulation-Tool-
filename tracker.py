from datetime import datetime
from models import db, Target


def record_click(token, ip_address, user_agent):
    """
    Records that a target clicked the phishing link.
    Captures metadata for the awareness report.

    🔐 SECURITY CONCEPT — Metadata Leakage:
       When you click a link, the server receives:
       - Your IP address (approximate location)
       - Your User-Agent (browser, OS, device type)
       - Timestamp (when you were active)
       Even WITHOUT entering credentials, clicking reveals data about you.
    """
    target = Target.query.filter_by(token=token).first()

    if target and not target.clicked:
        target.clicked = True
        target.clicked_at = datetime.utcnow()
        target.ip_address = ip_address
        target.user_agent = user_agent
        db.session.commit()
        return target
    return target
