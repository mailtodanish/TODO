
from .views import ScheduledActivityList
from .views import RevisionItem, RevisionItemUpdate, CommentsofTheDay
from .views import RevisionItemofTheDay, ChildActivityList, FavouriteItem,MakeTask
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .apiview import ActivityViewSet

from django.urls import path
urlpatterns = [
    # generates token only post method is allowed
    path('api/api-token-auth/', obtain_auth_token, name='api_token_auth'),
    # Test Case -Done
    path("api/activities/scheduled", ScheduledActivityList.as_view(),
         name="activity_api_list"),
    # in-use for making activity done
    path("api/revision/", RevisionItem.as_view(), name="revision_item"),
    # update updated field
    path("api/revision/<int:pk>/", RevisionItemUpdate.as_view(),
         name="revision_item_update"),
    # daily_task Test Case -done
    path("api/random_revision_item/", CommentsofTheDay.as_view(),
         name="daily_random_revision_item"),
    # daily_task Test Case -done
    path("api/dailytask/", RevisionItemofTheDay.as_view(),
         name="daily_task"),
     #child activities
    path("api/childactivity/<int:pk>/", ChildActivityList.as_view(),
         name="api-child-activity"),
    path("api/fav-items/", FavouriteItem.as_view(),
         name="api-fav-item"),
    path("api/project-task/", MakeTask.as_view(),
         name="api-task-item"),
]

# router has been used in activity creation API.
router = DefaultRouter()
# create activity - TEST Case -Done
router.register('ActivityRouter', ActivityViewSet, 'api-activity')
urlpatterns += router.urls
