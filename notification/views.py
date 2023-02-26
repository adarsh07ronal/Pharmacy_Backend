from rest_framework import viewsets
from .models import *
from .serializers import *

# Create your views here.
class NotificationViewset(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    # permission_classes = [IsAuthenticated]
    filterset_fields = ['status']

