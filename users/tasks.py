from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from drf_users_app import settings


@shared_task
def send_mail_to_verify_account(user_email, first_name, token):
    """ Task que manda o email de ativação de conta """

    send_mail(
        subject='Ativação de conta',
        from_email='from@example.com',
        message="",
        recipient_list=[user_email, ],
        html_message=f"<h3>Olá, {first_name},</h3>"
                     f"<p>Clique no link abaixo para ativar sua conta."
                     f"<a href='{settings.FRONTEND_URL}/activate-account/{token}'>ATIVAR CONTA</a>"
    )


@shared_task
def send_mail_to_reset_user_password(user_email, first_name, token):
    """ Task que manda email para redefinir a senha """

    send_mail(
        subject='Redefinição de senha',
        from_email='from@example.com',
        message="",
        recipient_list=[user_email, ],
        html_message=f"<h3>Olá, {first_name},</h3>"
                     f"<p>Clique no botão abaixo para redefinir sua senha.</p>"
                     f"<a href='{settings.FRONTEND_URL}/reset-password/{token}'>REDEFINIR SENHA</a>"
    )
