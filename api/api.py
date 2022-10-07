from rest_framework import generics
from projects.models import Activity
from .serializers import ActivitySerializer

# Using DRF generic views to simplify code
class ActivityListGeneric(generics.ListCreateAPIView):
        queryset = Activity.objects.all()
        serializer_class = ActivitySerializer

class ActivityDetailGeneric(generics.RetrieveDestroyAPIView):
        def get_queryset(self):
            queryset = Activity.objects.filter(pk=self.kwargs["pk"])
            return queryset
        serializer_class = ActivitySerializer

class ActivityCreate(generics.CreateAPIView):
         serializer_class = ActivitySerializer
