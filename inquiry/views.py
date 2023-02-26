from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets   
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.core.mail import send_mail
from inquiry.models import Inquiry, InquiryMessage
from inquiry.serializers import InquirySerializer,InquiryRetrieveSerializer

class InquiryViewSet(viewsets.ModelViewSet):
	queryset = Inquiry.objects.all()
	serializer_class = InquirySerializer
	# @swagger_auto_schema(
    #     request_body=openapi.Schema(
    #         type=openapi.TYPE_OBJECT,
    #         properties={
    #             'email': openapi.Schema(type=openapi.TYPE_STRING,
    #                                        description='email'),
    #             'contact_category': openapi.Schema(type=openapi.TYPE_INTEGER,
    #                                        description='contact category'),
    #             'name': openapi.Schema(type=openapi.TYPE_STRING,
    #                                        description='name'),
    #         	'contents_of_inquiry': openapi.Schema(type=openapi.TYPE_STRING,
    #                                        description='contents_of_inquiry'),
    #         },
    #         required=['contact_category', 'name', 'contents_of_inquiry'],
    #     ),
    #     responses={status.HTTP_200_OK:InquirySerializer}
    # )

	def list(self, request):
		queryset = Inquiry.objects.all()
		user =self.request.user
		if self.request.user.is_anonymous:
			queryset=[]
		else:
			if user.is_superuser:
				pass
			else:
				if user.is_patient:
					queryset = queryset.filter(inquiry_user=user)
				elif user.is_pharmacy:
					queryset = queryset.filter(inquiry_pharmacy__user=user)
		serializer = InquiryRetrieveSerializer(queryset, many=True)
		return Response(serializer.data)

	def create(self, request, *args, **kwargs):
		mutable = request.POST._mutable
		request.POST._mutable = True
		data = request.data
		if self.request.user.is_anonymous:
			send_mail("{} 様からメッセージが届いています。".format(data["name"]), "Category : {}\n\nContents of Inquiry : {}\n\nEmail : {}".format(data["contact_category"],data["contents_of_inquiry"],data["email"]), data["email"], ['developers.geitpl@gmail.com','r-kajiwara@automagic.co.jp','h-mizoguchi@automagic.co.jp','karre@eoraa.com'])
		if self.request.user:
			try:
				data["email"] = self.request.user.email
				if self.request.user.is_patient:
					data["inquiry_user"] = self.request.user.id
					send_mail("{} 様からメッセージが届いています。".format(data["name"]), "以下のURLからメッセージを確認してください。\n{}".format("https://dev-pharma-cms.eoraa.com/"), data["email"], ['developers.geitpl@gmail.com','r-kajiwara@automagic.co.jp','h-mizoguchi@automagic.co.jp','karre@eoraa.com'])
				elif self.request.user.is_pharmacy:
					if self.request.user.drugstore_user.all():
						data["inquiry_pharmacy"] = self.request.user.drugstore_user.all()[0].id
						send_mail("{} 様からメッセージが届いています。".format(data["name"]), "以下のURLからメッセージを確認してください。\n{}".format("https://dev-pharma-cms.eoraa.com/"), data["email"], ['developers.geitpl@gmail.com','r-kajiwara@automagic.co.jp','h-mizoguchi@automagic.co.jp','karre@eoraa.com'])
			except:
				pass
		serializer = InquirySerializer(data = data)
		if serializer.is_valid():
			Inquiry_obj = serializer.save(is_resolved=False)
			return Response(InquirySerializer(Inquiry_obj).data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisteredInquiryAPIView(APIView):
	def get(self,request,*args,**kwargs):
		inquiry_id = self.kwargs["id"]
		inquiry_objs = Inquiry.objects.filter(id=inquiry_id)
		if inquiry_objs.count():
			inquiry_obj = inquiry_objs.first()
			return Response(data=InquiryRetrieveSerializer(inquiry_obj).data,status=status.HTTP_200_OK)
		return Response({"message":"問い合わせデータが見つかりません"}, status=status.HTTP_404_NOT_FOUND)

class RegisteredInquiryCreateAPIView(APIView):
	"""
	Inquiry Reply APIView

	Request Data : {
		"message" : ""
	}
	"""
	def put(self,request,*args,**kwargs):
		inquiry_id = self.kwargs["id"]
		inquiry_objs = Inquiry.objects.filter(id=inquiry_id)
		if inquiry_objs.count():
			inquiry_obj = inquiry_objs.first()
			inquiry_obj.is_resolved=True
			inquiry_obj.save()
			InquiryMessage.objects.create(inquiry=inquiry_obj,message=self.request.data["message"],sender=self.request.user)
			return Response(data=InquiryRetrieveSerializer(inquiry_obj).data,status=status.HTTP_200_OK)
		return Response({"message":"問い合わせデータが見つかりません"}, status=status.HTTP_404_NOT_FOUND)
	
