from rest_framework import viewsets
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response

# Create your views here.
class MedicineTipsViewSet(viewsets.ModelViewSet):
    queryset = MedicineTips.objects.all()
    permission_classes=[IsAuthenticatedOrReadOnly]
    serializer_class = MedicineTipsSerializer
    parser_classes = (MultiPartParser,JSONParser)
    
    def list(self, request):
        queryset = MedicineTips.objects.all()
        serializer = MedicineTipsRtrieveSerializer(self.paginate_queryset(queryset), many=True)
        # return Response(serializer.data)
        return self.get_paginated_response(serializer.data)


    def retrieve(self, request, pk=None):
        queryset = MedicineTips.objects.all()
        queryset = get_object_or_404(queryset, pk=pk)
        serializer = MedicineTipsRtrieveSerializer(queryset,context={"request": request})
        return Response(serializer.data)

class MedicineTipsCategoryViewset(viewsets.ModelViewSet):
    queryset = MedicineTipsCategory.objects.all()
    permission_classes=[IsAuthenticated]
    # pagination_class = None
    serializer_class = MedicineTipsCategorySerializer
    # parser_classes = (MultiPartParser,JSONParser)
