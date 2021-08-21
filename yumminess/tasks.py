from celery import shared_task

from .slackmessage import slack_message


@shared_task
def send_slack_message_menu():
    slack_message("Testing slack messages")
    return None
