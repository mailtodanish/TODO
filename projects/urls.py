from django.urls import path
from .views import Home, SettingsLov, SettingsAddLov, SettingsDeleteLov
from .views import TaskList, AddTask, DeleteTask, TaskDetail, TaskUpdate
from .views import AddTaskComment, DeleteTaskCommnet, AddLink, TaskCommentList
from .views import TaskCommentUpdate
from .views import ActivityDetail, DeleteActivity, ActivityList, AddActivity
from .views import ActivityUpdate, CommentsDetail
from .views import CreateActivityFromHomePage, UserEditView
from . import views
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path('', views.login, name="login"),
    path('profile/', UserEditView.as_view(), name="edit_profile"),
    path("logout/", LogoutView.as_view(
        template_name='projects/registration/login.html'), name="logout"),
    path('Dashboard/', Home.as_view(), name="HomePage"),
    # Lov List View
    path('setting/lov/', SettingsLov.as_view(), name="lov-view"),
    # Add Lov
    path('setting/lov/add/', SettingsAddLov.as_view(), name='lov-add'),
    # Delete LOV
    path('setting/lov/<pk>/delete/', SettingsDeleteLov.as_view(
    ), name='lov-delete'),
    # Task List View
    path('task/', TaskList.as_view(), name="task-view"),
    # Add Task
    path('task/add/', AddTask.as_view(), name='task-add'),
    # Delete Task
    path('task/<pk>/delete/', DeleteTask.as_view(), name='task-delete'),
    # Task Detail
    path('task/<slug:slug>/', TaskDetail.as_view(), name='task-detail'),
    path('task/shared/<str:signed_slug>/', views.get_shareable_link,
         name='shared-task-detail'),
    path('task/update/<pk>/', TaskUpdate.as_view(), name='task_update'),
    # Add Task comment
    path('task/<pk>/comment/add/', AddTaskComment.as_view(),
         name='task-comment-add'),
    # Delete Task comment
    path('task/comment/<pk>/delete/', DeleteTaskCommnet.as_view(),
         name='task-comment-delete'),
    # Add Link
    path('link/add/', AddLink.as_view(), name='link-add'),
    # Add Activity
    path('activity/add/', AddActivity.as_view(), name='activity-add'),
    # Add Activity from comment
    path('activity/add/<pk>', AddActivity.as_view(),
         name='comment-activity-add'),
    # Activity List View
    path('activity/', ActivityList.as_view(), name="activity-view"),
    # Activity List View - scheduled
    path('activity/<slug:slug>', ActivityList.as_view(),
         name="activity-scheduled"),
    # Detail of Activity
    path('activity/<pk>/', ActivityDetail.as_view(), name='activity-detail'),
    # Delete Task
    path('activity/<pk>/delete/', DeleteActivity.as_view(),
         name='activity-delete'),
    path('activity/update/<pk>/', ActivityUpdate.as_view(),
         name='activity_update'),
    # Task List View & used in tags serach
    path('comments/', TaskCommentList.as_view(), name="task-comments-view"),
    # search on top banner
    path('comments/<slug:slug>/', TaskCommentList.as_view(), name="tagged"),
    path('comments/update/<pk>/', TaskCommentUpdate.as_view(),
         name='comment_update'),
    # it shows only one record
    path('revision/', CommentsDetail.as_view(), name='revise-comments'),
    # it shows only one record
    path('revision/<pk>', CommentsDetail.as_view(),
         name='revise-update-comments'),
    path('task/<slug:slug>/pdf/', login_required(views.generate_pdf),
         name='task_as_pdf'),
    # Add Activity from Home Page
    path('ActivityFromHomePage/addFromHomePage/',
         CreateActivityFromHomePage.as_view(), name='activity-add-homepage'),
    path('signup/', views.signup, name='signup'),
]
