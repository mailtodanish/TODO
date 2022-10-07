''' signals '''
from django.utils import timezone


def task_updated(sender, **kwargs):
    ''' update task '''
    _obj = kwargs.pop('instance')
    task = _obj.task
    task.updated_at = timezone.now()
    task.save()

