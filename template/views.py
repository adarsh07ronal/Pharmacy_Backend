from rest_framework import viewsets
from .serializers import TemplateSerializer,TemplateCreateSerializer
from .models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class TemplateViewset(viewsets.ModelViewSet):
    """
    Template CRUD APIs

    POST Data : {
        "user" : 1,
        "title" : "",
        "body" : ""
    }

    PUT Data : {
        "title" : "",
        "body" : ""
    }

    """

    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        qs = Template.objects.filter(user=self.request.user)
        return qs

    def create(self, request, *args, **kwargs):
        try:
            mutable = request.POST._mutable
            request.POST._mutable = True
            data = request.data
            user_obj = self.request.user
            data["user"] = user_obj.id
            serializer = TemplateCreateSerializer(data=data)

            if serializer.is_valid():
                instance = serializer.save()
                return Response(data = TemplateSerializer(instance).data ,status=status.HTTP_201_CREATED)
            else:
                return Response(data = serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def update(self, request, pk):
        try:
            temp_obj = Template.objects.filter(id=pk)
            if temp_obj.count():
                temp_obj = temp_obj.first()
                data = request.data
                serializer = TemplateSerializer(temp_obj,data=data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(data = serializer.data ,status=status.HTTP_202_ACCEPTED)
                else:
                    return Response(data = serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            return Response({"message":"テンプレートデータが見つかりません"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 