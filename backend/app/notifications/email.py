# backend/app/notifications/email.py

import logging
import resend
from django.conf import settings

logger = logging.getLogger(__name__)


def send_ticket_reply_email(*, to_email: str, ticket_id: int) -> bool:
    """
    Sends a "you have a new reply" notification email to a customer whose
    ticket got an agent reply. Returns True/False instead of raising -
    email delivery must never break the agent's reply flow, the same way
    AI failures never break ticket creation elsewhere in this app.
    """
    if not settings.RESEND_API_KEY:
        logger.warning(
            "RESEND_API_KEY not configured - skipping email for ticket_id=%s",
            ticket_id,
        )
        return False

    resend.api_key = settings.RESEND_API_KEY

    try:
        resend.Emails.send(
            {
                "from": settings.NOTIFICATION_FROM_EMAIL,
                "to": [to_email],
                "subject": "You have a new reply on your support ticket",
                "text": (
                    "Hi,\n\n"
                    "Our support team has just replied to your ticket.\n\n"
                    "Please revisit the chat widget on our website to view "
                    "the reply and continue the conversation.\n\n"
                    "Thanks,\n"
                    "Resolvio Support"
                ),
            }
        )
        logger.info(
            "Reply notification email sent: ticket_id=%s to=%s", ticket_id, to_email
        )
        return True
    except Exception:
        logger.exception(
            "Failed to send reply notification email: ticket_id=%s to=%s",
            ticket_id,
            to_email,
        )
        return False
