'''
Activity API View
FIXME: C0114: Missing module docstring (missing-module-docstring)
'''
from rest_framework import generics
from projects.models import Activity
from .serializers import ActivitySerializer


class ActivityListGeneric(generics.ListCreateAPIView):
    """
    Activity List
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


class ActivityDetailGeneric(generics.RetrieveDestroyAPIView):
    """
    Activity Detail
    """

    def get_queryset(self):
        queryset = Activity.objects.filter(pk=self.kwargs["pk"])
        return queryset
    serializer_class = ActivitySerializer


class ActivityCreate(generics.CreateAPIView):
    """
    Create activity
    """
    serializer_class = ActivitySerializer
