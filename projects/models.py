import datetime

from django.conf import settings
from django.core.signing import Signer
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django_cryptography.fields import encrypt
from taggit.managers import TaggableManager
from tinymce.models import HTMLField
from unidecode import unidecode
from slack import WebClient


class TimeAuditModel(models.Model):
    """ To path when the record was created and last modified """
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
    )
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name="Last Modified At")

    class Meta:
        abstract = True


class ApplictaionData(models.Model):
    '''
    It will store applictaion related data
    static list of value
    TestCase - Done
    '''
    Name = models.CharField(max_length=200,
                            null=False,
                            verbose_name="name",
                            help_text="list of value - name")
    Value = models.CharField(max_length=200,
                             null=False,
                             verbose_name="value",
                             help_text="list of value - value")
    IsCategory = models.BooleanField(null=True,
                                     verbose_name="category",
                                     help_text="list of value - category")
    Type = models.ForeignKey('self',
                             on_delete=models.CASCADE,
                             null=True,
                             verbose_name="type")
    Description = models.CharField(max_length=200,
                                   null=False,
                                   verbose_name="description",
                                   help_text="list of value - description ")

    def get_absolute_url(self):
        return reverse('lov-view')

    def __str__(self):
        return self.Name


def generate_unique_slug(_class, field):
    origin_slug = slugify(field)
    unique_slug = origin_slug
    numb = 1
    while _class.objects.filter(slug=unique_slug).exists():
        unique_slug = '%s-%d' % (origin_slug, numb)
        numb += 1
    return unique_slug


class ProjectTask(TimeAuditModel):
    '''
    It will store major task and related info as comment and timeline
    '''
    Task_Description = models.CharField(max_length=200,
                                        null=False,
                                        unique=True,
                                        verbose_name="description",
                                        help_text="task description")
    Task_Title = models.TextField(null=False, unique=True)
    fav_flag = models.BooleanField(default=False, null=True)

    signer = Signer(salt='projectTask.Task')
    slug = models.SlugField(max_length=200, unique=True, null=True)

    def __str__(self):
        return self.Task_Title

    @classmethod
    def get_signed_hash(self):
        '''signed hashed'''
        signed_pk = self.signer.sign(self.slug)
        return signed_pk

    @classmethod
    def get_absolute_url(self):
        '''get absolute url'''
        return reverse('shared-task-detail', args=(self.get_signed_hash(), ))

    def save(self, *args, **kwargs):
        task_title = unidecode(self.Task_Title)
        if self.slug:
            if slugify(task_title) != self.slug:
                self.slug = generate_unique_slug(ProjectTask, task_title)
        else:
            self.slug = generate_unique_slug(ProjectTask, task_title)
        super().save(*args, **kwargs)


class TaskComment(models.Model):
    '''
    It will store task related data
    and timeline
    '''
    fav_flag = models.BooleanField(default=False, null=True)
    task_flag = models.BooleanField(default=False, null=True)
    content = encrypt(HTMLField(null=True))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(default=timezone.now)
    tags = TaggableManager(blank=True)
    signer = Signer(salt='projectTask.Task')
    task = models.ForeignKey(ProjectTask,
                             on_delete=models.CASCADE,
                             related_name="task_comment",
                             blank=True,
                             null=True)

    def get_signed_hash(self):
        '''signed hash'''
        signed_pk = self.signer.sign(self.task.slug)
        return signed_pk

    def get_absolute_url(self):
        return reverse('task-detail', args=(self.get_signed_hash(), ))

    def save(self, *args, **kwargs):
        self.updated = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
       ordering = ['-fav_flag', '-pk']


class FavLink(models.Model):
    '''
    Favourite link
    '''
    name = models.CharField(max_length=200, null=False, unique=True)
    link = models.CharField(max_length=200, default="no link")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Activity(models.Model):
    '''
    Activities
    '''
    Title = models.CharField(max_length=200, null=False, unique=True)
    Description = models.TextField()
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    status = models.CharField(max_length=100, default='Open')
    Type = models.CharField(max_length=100, default='General', null=True)
    scheduled = models.DateTimeField(default=timezone.now, null=True)
    # updated at and it will be popuplated on save()
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    # stores id of parent activity for scheduled activity.
    parentActivityId = models.IntegerField(null=True, unique=False, default=0)

    @property
    def isScheduled(self):
        '''
        property : if scheduled activity is scheduled or have past date.
        '''
        if self.Type != "General":
            if timezone.localtime() > timezone.localtime(self.scheduled):
                return True
            else:
                return False
        else:
            return False

    def __str__(self):
        return self.Title

    def get_absolute_url(self):
        return reverse('activity-detail', args=[self.pk])

    def day_hence(self, number_of_days):
        return timezone.now() + timezone.timedelta(days=number_of_days)

    def save(self, *args, **kwargs):
        # update column
        self.updated = timezone.now()
        super().save(*args, **kwargs)
        if self.status == "Done" and self.parentActivityId != 0:
            # search activity and update rescheduled date
            # for scheduled activities.
            scheduledActivity = Activity.objects.get(pk=self.parentActivityId)
            # if parent activity is schedule for weekly
            if scheduledActivity.Type == 'Weekly':
                # update Scheduled Date
                scheduledActivity.scheduled = self.day_hence(3)
            elif scheduledActivity.Type == 'Monthly':
                # update Scheduled Date
                scheduledActivity.scheduled = self.day_hence(30)
            elif scheduledActivity.Type == 'Yearly':
                # update Scheduled Date
                scheduledActivity.scheduled = self.day_hence(365)
            scheduledActivity.Description = self.Description
            scheduledActivity.save()



class Favoutite_item(models.Model):
    '''
    It will store favourite items
    '''
    type = models.CharField(max_length=50, null=True)
    item_id = models.CharField(max_length=50, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        # update column
        super().save(*args, **kwargs)
        if self.type == "task":
            task: ProjectTask = ProjectTask.objects.get(pk=self.item_id)
            task.fav_flag = True
            task.save()
        if self.type == "comment":
            comment: TaskComment = TaskComment.objects.get(pk=self.item_id)
            comment.fav_flag = True
            comment.save()

    def delete(self, *args, **kwargs):
        # update column
        if self.type == "task":
            task: ProjectTask = ProjectTask.objects.get(pk=self.item_id)
            task.fav_flag = False
            task.save()
        if self.type == "comment":
            comment: TaskComment = TaskComment.objects.get(pk=self.item_id)
            comment.fav_flag = False
            comment.save()

        super().delete(*args, **kwargs)