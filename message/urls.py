from message import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register("message",views.MessageCreateAPI)

urlpatterns = [

] + router.urls