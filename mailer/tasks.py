import base64
import traceback

from celery import shared_task
from django.core.mail import EmailMessage
from django.utils import timezone

from mailer.choices import ScheduledEmailStatusChoices
from mailer.models import ScheduledEmail


@shared_task
def schedule_send_email(
    subject: str,
    content: str,
    from_email: str,
    recipient_list: list,
    email_instance: ScheduledEmail,
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

    try:
        msg.send(fail_silently=False)
    except Exception:
        ScheduledEmail.objects.filter(pk=email_instance).update(
            status=ScheduledEmailStatusChoices.FAILED.value,
            message=traceback.format_exc(),
        )
    else:
        ScheduledEmail.objects.filter(pk=email_instance).update(
            status=ScheduledEmailStatusChoices.SENT.value,
            message='Mail sent successfully',
            timestamp=timezone.now()
        )
