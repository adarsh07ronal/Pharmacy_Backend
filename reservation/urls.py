from django.urls import path
from .views import ForReservationViewset,ForReservationReplyAPI, RecieveChoiceAPIView,PrescriptionReservationSearchAPI, GuidanceMessageViewset,UserMemoViewset
from rest_framework import routers

router = routers.SimpleRouter()
router.register("for_reservation",ForReservationViewset)
router.register("guidance_message",GuidanceMessageViewset)
router.register("user_memo_api",UserMemoViewset,basename='user_memo_api')
# router.register("for_reservation/reply",ForReservationReplyViewset)

urlpatterns = [
    path('',ForReservationReplyAPI.as_view()),
    path('recieve_choice/',RecieveChoiceAPIView.as_view()),
    path('prescription_reservation/search/',PrescriptionReservationSearchAPI.as_view()),
] + router.urls
