import json
import os
from functools import partial

from django.conf import settings
from django.core.files import File
from django.template.loader import render_to_string

from helpers.short_func import get_file_type_by_extension
from mailer.models import ScheduledEmail
from mailer.tasks import schedule_send_email


class Mailer:
    _scheduler = schedule_send_email.delay
    _base_subject_path = settings.BASE_DIR / 'mailer' / 'templates' / 'subject'
    _base_content_path = settings.BASE_DIR / 'mailer' / 'templates' / 'content'

    def __init__(self):
        self.attachments = []

    def __call__(self, to: list, template_name: str, from_email: tuple = None, system_mail: bool = True, attachments: list = None, **context):
        self.sender = from_email or settings.DEFAULT_FROM_EMAIL
        self.receivers = to

        subject_path = self._base_subject_path / f'{template_name}.txt'
        if os.path.isfile(subject_path):
            subject = render_to_string(subject_path, context=context)
        else:
            subject = context.get('subject', None)

        content_path = self._base_content_path / f'{template_name}.html'
        if os.path.isfile(content_path):
            content = render_to_string(content_path, context=context)
        else:
            content = context.get('content', None)

        if subject is None or content is None:
            raise ValueError('`subject` and `content` must be defined')
        # generate an instance
        instance = ScheduledEmail.objects.create(
            system_generated=system_mail,
            receivers=json.dumps(self.receivers),
            sender=json.dumps(self.sender),
            subject=subject,
            content=content,
        )
        # clear previous attachments
        self.clear_attachments()
        # declare the function
        _scheduled_email = partial(
            self._scheduler,
            recipient_list=self.receivers,
            email_instance=instance.pk,
            from_email=self.sender,
            subject=subject,
            content=content
        )

        for attachment in attachments or []:
            self.add_attachment(attachment)

        _scheduled_email(
            attachments=self.attachments
        )

    def add_attachment(self, file: File):
        filename = file.name
        file_obj = file.open(mode='rb')
        content = file_obj.read()
        file_obj.close()
        mime_type = get_file_type_by_extension(file)
        self.attachments.append({
            'filename': filename,
            'content': content,
            'mime_type': mime_type,
        })

    def clear_attachments(self):
        self.attachments = []


schedule_email = Mailer()
