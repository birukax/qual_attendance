# # from __future__ import absolute_import, unicode_literals
# import os
# import sys
# from celery import Celery
# from django.conf import settings

# # from django.apps import apps

# # set the default django setting module for the 'celery' program.

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qual.settings.prod")
# broker_connection_retry_on_startup = True
# app = Celery(
#     "qual",
#     broker="redis://redis:6379",
#     backend="redis://redis:6379",
#     # include=["qual.attendance.tasks"],
# )
# # app.config_from_object(settings, namespace="CELERY")
# app.config_from_object("django.conf:settings", namespace="CELERY")
# app.autodiscover_tasks()
# # app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
# # app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])


# @app.task(bind=True)
# def debug_task(self):
#     print(f"Request: {self.request!r}")
