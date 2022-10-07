from django.contrib import admin
from .models import ApplictaionData,ProjectTask,TaskComment,FavLink,Activity,Favoutite_item


from django.contrib import admin

from .models import ApplictaionData, ProjectTask, TaskComment, FavLink, Activity, Favoutite_item


@admin.register(ApplictaionData)
class ApplictaionDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'Name',
        'Value',
        'IsCategory',
        'Type',
        'Description',
    )
    list_filter = ('IsCategory', 'Type')


@admin.register(ProjectTask)
class ProjectTaskAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'updated_at',
        'Task_Description',
        'Task_Title',
        'fav_flag',
        'is_active',
        'slug',
    )
    list_filter = ('created_at', 'updated_at', 'fav_flag', 'is_active')
    search_fields = ('slug',)
    date_hierarchy = 'created_at'


@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'fav_flag',
        'task_flag',
        'content',
        'created',
        'updated',
        'task',
    )
    list_filter = ('fav_flag', 'task_flag', 'created', 'updated')
    raw_id_fields = ('task',)


@admin.register(FavLink)
class FavLinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'link', 'created')
    list_filter = ('created',)
    search_fields = ('name',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'Title',
        'Description',
        'created',
        'status',
        'Type',
        'scheduled',
        'updated',
        'parentActivityId',
    )
    list_filter = ('created', 'scheduled', 'updated', 'status')


@admin.register(Favoutite_item)
class Favoutite_itemAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'item_id', 'created', 'updated')
    list_filter = ('created', 'updated')
