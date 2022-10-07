from rest_framework import viewsets
from projects.models import Activity,TaskComment,ProjectTask
from .serializers import ActivitySerializer,TaskCommentSerializer,TaskSerializer
from rest_framework import authentication, permissions
from django.utils import timezone

class ActivityViewSet(viewsets.ModelViewSet):
        '''
        ActivityRouter - Test Case - Done
        '''
        dt = timezone.now()
        queryset = Activity.objects.filter(
                scheduled__lte=dt, Type='General').exclude(
                    status='Done').order_by('-scheduled')
        serializer_class = ActivitySerializer
        permission_classes = (permissions.IsAuthenticated,)


class TaskCommentViewSet(viewsets.ModelViewSet):
        queryset = TaskComment.objects.all()
        serializer_class = TaskCommentSerializer
        permission_classes = (permissions.IsAuthenticated,)

class TaskViewSet(viewsets.ModelViewSet):
        queryset = ProjectTask.objects.all()
        serializer_class = TaskSerializer
        permission_classes = (permissions.IsAuthenticated,)
