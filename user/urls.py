from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'login', views.LoginViewSet, basename='login')
router.register(r'logout', views.LogoutViewSet, basename='logout')
router.register(r'verify-register-user-otp', views.RegistrationOtpVerificationViewSet, basename='verify_reg_user_otp')
router.register(r'forgot-password', views.ForgotPasswordViewSet, basename='forgot_password')
router.register(r'verify-and-reset-otp-forgot-password-reset', views.ForgotPasswordOtpVerificationAndResetPasswordViewSet, basename='verify_forgot_pass_otp')
router.register(r'reset-password', views.ResetPasswordViewSet, basename='reset_password')


urlpatterns = [
    path('', include(router.urls)),
]
