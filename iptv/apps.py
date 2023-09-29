import os
import time
from threading import Thread

from django.apps import AppConfig


class IptvConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "iptv"

    def ready(self):
        from iptv import api_dl

        if not os.environ.get("RUN_MAIN"):
            return

        try:  # default to 5 minute loop
            loop_delay = int(os.environ.get("LOOP_DELAY", 300))
        except ValueError:
            loop_delay = 300

        def loop():
            while True:
                print("Downloading video data")
                api_dl.download_all()
                print("Downloading video data finished")
                time.sleep(loop_delay)

        t = Thread(target=loop, daemon=True)
        t.start()
