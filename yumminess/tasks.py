from .slackmessage import slack_message
from celery import shared_task
from datetime import date
from .models import SlackMessage


@shared_task
def send_slack_message_menu():
    sent = False
    current_date = date.today()
    slack_message_object = SlackMessage.objects.get(created_at=current_date)

    # Sends slack message to slack channel for chilean employees.
    if not slack_message_object.sent:
        status_code = slack_message(slack_message_object.message_text)
        if status_code == 200:
            slack_message_object.sent = True
            slack_message_object.save()
            sent = True

    return sent
