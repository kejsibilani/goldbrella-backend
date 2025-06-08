import base64

from celery import shared_task
from django.core.mail import EmailMessage


@shared_task
def schedule_send_email(
    subject: str,
    content: str,
    from_email: str,
    recipient_list: list,
    attachments: list = None,
):
    """
    Send an HTML email, optionally with attachments.
    attachments: list of dicts with keys 'filename','content' (base64 str), and optional 'mimetype'
    """
    msg = EmailMessage(
        subject=subject,
        body=content,
        from_email=from_email,
        to=recipient_list,
    )
    msg.content_subtype = "html"  # important!

    if attachments:
        for attachment in attachments:
            name = attachment["filename"]
            data = base64.b64decode(attachment["content"])
            mimetype = attachment.get("mimetype", None)
            msg.attach(name, data, mimetype)
    msg.send(fail_silently=False)
