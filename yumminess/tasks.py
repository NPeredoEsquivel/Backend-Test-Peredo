from .slackmessage import slack_message
from celery import shared_task
from datetime import date

@shared_task
def send_slack_message_menu():
    slack_message("Testing slack messages")
    return None


@shared_task
def create_slack_message():

    slack_message("Se ha creado el mensaje de slack para poder enviarlo")
    return None

