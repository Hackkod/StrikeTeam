# team/tasks.py
from celery import shared_task
import time


@shared_task
def display_image_task():
    print("Displaying image on screen")
    time.sleep(1)
    print("Image hidden")
