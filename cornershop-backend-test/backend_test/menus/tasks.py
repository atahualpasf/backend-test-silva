"""Menu tasks."""

# Celery
from celery.task import task
# Django
from django.conf import settings
from django.utils import timezone

# Python
import pytz
# Slack
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


@task(name="send_menu_public_url", max_retries=3)
def send_menu_public_url_task(data, text):
    """Sey hello test with celery."""

    timezone.activate(timezone=pytz.timezone("America/Santiago"))
    client = WebClient(token=settings.SLACK_BOT_TOKEN)

    try:
        response = client.chat_postMessage(channel="general", blocks=data, text=text)
    except SlackApiError as e:
        assert e.response["error"]
