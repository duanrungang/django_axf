from celery import shared_task

from FruitGP2.utils import send_activate_email


@shared_task
def send_activate_email_async(username, to_email):
    send_activate_email(username, to_email)
