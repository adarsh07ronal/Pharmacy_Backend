# Authentication
from django.urls import path, include
from pharmacy_auth import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register('patient/signup',views.PatientSignupViewSet,basename='patient_signup')
router.register('orthrus/signup',views.OrthrusSignupViewSet, basename='orthrus_signup')
router.register('pharmacy/signup',views.PharmacySignupViewSet,basename='pharmacy_signup')

urlpatterns = [
	path('',include(router.urls)),
	path('forgot_password/',views.ForgotPasswordOtpApi.as_view(), name='forgot_password'),
	path('verify_otp/',views.VerifyOtpApi.as_view(), name='verify_otp'),
	path('reset_password/',views.ResetPasswordApi.as_view(), name='reset_password'),
	path('change_password/',views.ChangePasswordApi.as_view(),name='change_password'),
	path('patient/login/',views.PatientLoginApiView.as_view(), name='patient_login'),
	path('email/verification/',views.EmailVerification.as_view(), name='email_verification'),
	path('reset/password/',views.ResetPasswordVerification.as_view(), name='reset_pass_ver'),
	path('user/management/status/',views.AdministratorStatusAPIView.as_view(), name='user_management_status'),
	path('user/management/',views.OrthrusUserManagementApiView.as_view(), name='user_management'),
	path('registered/user_management/',views.RegisteredUserManagement.as_view(), name='registered_user_management'),
	path('registered/pharmacy_management/',views.RegisteredPharmacyManagement.as_view(), name='registered_pharmacy_management'),
	path('user/management/<int:id>/',views.OrthrusUserManagementRetrieveUpdateDeleteAPIView.as_view(), name='user_management_update_delete'),
	path('cms/<int:id>/',views.CMSUserUpdateAPIView.as_view(), name='cms_update'),
	path('cms/login/',views.CMSLoginApiView.as_view(), name='cms_login'),
	path('pharmacy/login/',views.PharmacyLoginApiView.as_view(), name='pharmacy_login'),
	path('line/auth/',views.LineAuthAPIView.as_view(), name='line_auth'),
	path('dashboard/',views.DashboardAPIView.as_view(), name='dashboard'),
]



