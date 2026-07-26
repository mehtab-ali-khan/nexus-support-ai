# backend/app/notifications/email.py

import logging
import resend
from django.conf import settings

logger = logging.getLogger(__name__)


def _build_html_body(*, company_name: str) -> str:
    return f"""\
<!DOCTYPE html>
<html>
  <head>
    <meta name="color-scheme" content="light">
    <meta name="supported-color-schemes" content="light">
  </head>
  <body style="margin:0; padding:0; background-color:#f4f5f7; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" bgcolor="#f4f5f7" style="background-color:#f4f5f7; padding:32px 16px;">
      <tr>
        <td align="center">
          <table role="presentation" width="480" cellpadding="0" cellspacing="0" bgcolor="#ffffff" style="max-width:480px; width:100%; background-color:#ffffff; border-radius:14px; overflow:hidden; box-shadow:0 4px 16px rgba(0,0,0,0.08);">

            <!-- Header — brand gradient -->
            <tr>
                <td
                    bgcolor="#0f8a5b"
                    style="padding:28px 32px; background-color:#0f8a5b; background-image:linear-gradient(135deg, #0f8a5b, #1fd1ab);"
                >
                    <p style="margin:0; font-size:16px; font-weight:700; color:#ffffff; letter-spacing:-0.01em;">
                    {company_name}
                    </p>
                    <p style="margin:2px 0 0 0; font-size:12px; font-weight:600; color:rgba(255,255,255,0.85); text-transform:uppercase; letter-spacing:0.05em;">
                    Support
                    </p>
                </td>
            </tr>

            <!-- Body -->
            <tr>
              <td bgcolor="#ffffff" style="padding:32px; background-color:#ffffff;">
                <p style="margin:0 0 16px 0; font-size:15px; line-height:1.6; color:#111827;">
                  Hi there,
                </p>
                <p style="margin:0 0 26px 0; font-size:15px; line-height:1.6; color:#374151;">
                  Our support team has just replied to your message. Head back
                  to the chat to view the reply and continue the conversation.
                </p>
              </td>
            </tr>

            <!-- Footer -->
            <tr>
              <td bgcolor="#f9fafb" style="padding:18px 32px; background-color:#f9fafb; border-top:1px solid #e5e7eb;">
                <p style="margin:0; font-size:12px; line-height:1.5; color:#9ca3af;">
                  This is an automated message from {company_name}'s support team.
                </p>
              </td>
            </tr>

          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
"""


def _build_text_body(*, company_name: str) -> str:
    return (
        f"Hi there,\n\n"
        f"Our support team at {company_name} has just replied to your message.\n\n"
        f"Please revisit the chat to view the reply and continue the conversation.\n\n"
        f"— {company_name} Support"
    )


def send_ticket_reply_email(
    *, to_email: str, ticket_id: int, company_name: str
) -> bool:
    """
    Sends a "you have a new reply" notification email to a customer whose
    ticket got an agent reply. Returns True/False instead of raising -
    email delivery must never break the agent's reply flow, the same way
    AI failures never break ticket creation elsewhere in this app.

    The email is branded with the COMPANY's name, not "Resolvio" - the
    end customer only knows the company they contacted, and has no idea
    Resolvio (the platform powering that company's support) even exists.
    """
    if not settings.RESEND_API_KEY:
        logger.warning(
            "RESEND_API_KEY not configured - skipping email for ticket_id=%s",
            ticket_id,
        )
        return False

    resend.api_key = settings.RESEND_API_KEY

    from_address = f"{company_name} <{settings.NOTIFICATION_FROM_EMAIL}>"

    try:
        resend.Emails.send(
            {
                "from": from_address,
                "to": [to_email],
                "subject": f"New reply from {company_name} support",
                "html": _build_html_body(company_name=company_name),
                "text": _build_text_body(company_name=company_name),
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
