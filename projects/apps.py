'''app config'''

from django.apps import AppConfig
from django.db.models.signals import post_save


class ProjectsConfig(AppConfig):
    '''project config'''
    name = 'projects'

    def ready(self):
        super().ready()
        self._update_task_signals()

    @classmethod
    def _update_task_signals(cls):
        from .models import TaskComment
        from .signals import task_updated
        post_save.connect(receiver=task_updated, sender=TaskComment)
