# ecard/apps.py
from django.apps import AppConfig


class EcardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # Use 64-bit integer auto field for primary keys
    name = 'ecard'  # Ensure this matches the directory name and app path
