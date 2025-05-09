from celery import shared_task
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(dotenv_path=Path(__file__).resolve().parent / "env.bot")


@shared_task
def notify_completed_task():
    pass


"""
если вы предоставите информацию, я это реализую, в постановке задачи не совсем понятно,
что за уведомления должны приходить через Celery
"""
