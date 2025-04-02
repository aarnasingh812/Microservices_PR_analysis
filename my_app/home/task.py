from celery import Celery
from celery import shared_task

app=Celery('my_app')
app.config_from_object('django.config:settings', namespace="CELERY")
from home.utils.github import analyse_pr

@shared_task
def analyse_repo_task(repo_url, pr_number, github_token = None):
    results = analyse_pr(repo_url, pr_number, github_token=None)
    return results