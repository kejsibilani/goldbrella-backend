from datetime import datetime

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import localtime
from django_celery_beat.utils import make_aware
from django_rest_passwordreset.signals import reset_password_token_created

from account.models import User
from mailer.scripts import schedule_email
from mailer.system import system_info
from shift.models import Shift


@receiver(post_save, sender=User)
def create_shift_for_staff(instance, created, **kwargs):
    if created and instance.is_staff:
        Shift.objects.get_or_create(
            user=instance,
            defaults={
                'zone': None,
                'start_time': localtime(
                    make_aware(
                        datetime(1979, 1, 1, 9, 0, 0)
                    )
                ),
                'end_time': localtime(
                    make_aware(
                        datetime(1979, 1, 1, 17, 0, 0)
                    )
                ),
            }
        )


@receiver(reset_password_token_created)
def password_reset_token_created(instance, reset_password_token, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param kwargs: View Class Instance that sent the signal and other arguments
    """

    # send an e-mail to the user
    context = {
        'email': reset_password_token.user.email,
        'current_user': reset_password_token.user,
        'reset_password_token': reset_password_token.key,
        'reset_password_link': f"{instance.request._current_scheme_host}"
                               f"/auth/validate/?token="
                               f"{reset_password_token.key}"
    }

    schedule_email(
        expiration_time=getattr(settings, 'PASSWORD_RESET_TOKEN_EXPIRY_TIME'),
        support_link=f"{instance.request._current_scheme_host}/support",
        password_link=context['reset_password_link'],
        template_name='reset_password',
        user=context['current_user'],
        to=[context['email']],
        company=system_info,
        system_mail=True
    )
    return
