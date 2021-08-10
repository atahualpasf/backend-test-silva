"""Slack views."""

import json

# Django
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_str


def index(request):
    # menu_options = [
    #     {"option": 1, "name": "Corn pie, Salad and Dessert"},
    #     {"option": 2, "name": "Chicken Nugget Rice, Salad and Dessert"},
    #     {"option": 3, "name": "Rice with hamburger, Salad and Dessert"},
    #     {"option": 4, "name": "Premium chicken Salad and Dessert."},
    # ]
    # data = json.loads(
    #     force_str(
    #         render_to_string(
    #             "menus/menus/slack/today_reminder.json",
    #             {"action_url": "https://google.com", "menu_options": menu_options},
    #         ).strip()
    #     )
    # )
    # text = force_str(
    #     render_to_string(
    #         "menus/menus/slack/today_reminder_text.html",
    #         {"action_url": "https://google.com", "menu_options": menu_options},
    #     ).strip()
    # )
    # print(data)
    # print(text)
    # send_menu_public_url.delay(data, text)

    # ERROR_KEY = "ERROR"
    # try:
    #     from celery.task.control import inspect

    #     insp = inspect()
    #     d = insp.stats()
    #     if not d:
    #         d = {ERROR_KEY: "No running Celery workers were found."}
    # except IOError as e:
    #     from errno import errorcode

    #     msg = "Error connecting to the backend: " + str(e)
    #     if len(e.args) > 0 and errorcode.get(e.args[0]) == "ECONNREFUSED":
    #         msg += " Check that the RabbitMQ server is running."
    #     d = {ERROR_KEY: msg}
    # except ImportError as e:
    #     d = {ERROR_KEY: str(e)}
    # print(d)

    return HttpResponse(f"Hola mundo {timezone.now()}")
