from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from template.models import Template
from message.serializers import *
from message.models import ReservationMessage, TemplateReservationMessage

from rest_framework.permissions import IsAuthenticated


# Create your views here.
class MessageCreateAPI(viewsets.ModelViewSet):
    """
        Request Data : {
            "sender" : 1,
            "template" : 1,
            "message" : "Hello",
            "prescription_reservation" : 1
        }
    """
    queryset = ReservationMessage.objects.all().order_by('-updated_at')
    serializer_class = ReservationMessageSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            mutable = request.POST._mutable
            request.POST._mutable = True
            data = request.data
            template_data = data["template"]
            del data["template"]
            serializer = ReservationMessageSerializer(data=data)
            if serializer.is_valid():
                instance = serializer.save()
                template_instance = Template.objects.filter(id=template_data)
                if template_instance.count():
                    template_instance = template_instance.first()
                    TemplateReservationMessage.objects.create(template=template_instance,reservation_message=instance)
                return Response(data = ReservationMessageRetrieveSerializer(instance).data ,status=status.HTTP_201_CREATED)
            else:
                return Response(data = serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

    def list(self, request, *args, **kwargs):
        qs= ReservationMessage.objects.all().order_by('-updated_at')
        return Response(ReservationMessageRetrieveSerializer(qs,many=True).data)