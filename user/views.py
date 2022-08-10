from django.contrib.auth import authenticate
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from . models import User, RegisterUserOtp, ForgotPasswordOtp
from . serializers import UserSerializer, RegisterUserOtpSerializer, ForgotPasswordOtpSerializer, LoginSerializer, RegisterOtpSerializer, ForgotPasswordSerializer, ForgotPasswordOtpVerifyAndResetPasswordSerializer, ResetPasswordSerializer
from . services import send_auth_mail, generate_otp
from . permissions import UserAccessPermission
from . pagination import CustomPagination


class UserViewSet(viewsets.ViewSet):
    permission_classes_by_action = {
        'list': [IsAdminUser], 
        'retrieve': [UserAccessPermission | IsAdminUser],
        'create': [AllowAny],
        'update': [UserAccessPermission],
        'partial_update': [UserAccessPermission],
        'destroy': [UserAccessPermission]
    }

    def list(self, request):
        paginator = CustomPagination()
        queryset = User.objects.all()
        context = paginator.paginate_queryset(queryset, request)
        serializer = UserSerializer(context, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(request, user) # Applying the object level permission checking
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            otp = generate_otp()
            send_auth_mail("Register OTP", f" Hello {serializer.data['name']}, your registration OTP is {otp}", [serializer.data['email']])
            otp_serializer = RegisterUserOtpSerializer(data={'user':serializer.data['id'], 'otp':otp})
        
            if otp_serializer.is_valid():
                otp_serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) 

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        
        if not user.is_active:
            return Response({'message': 'Your account is not verified, verify it first.'}, status=status.HTTP_400_BAD_REQUEST)
            
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user, data=request.data, partial=True) # just because of some reason, this partial is used

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        
        if not user.is_active:
            return Response({'message': 'Your account is not verified, verify it first.'}, status=status.HTTP_400_BAD_REQUEST)
        
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
       
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(request, user)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Applying permission classes based on per viewSet method
    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


# API Login ViewSet

class LoginViewSet(viewsets.ViewSet):
    
    def create(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        queryset = User.objects.all()
        user = get_object_or_404(queryset, email=serializer.data['email'])
        user_serializer = UserSerializer(user)

        if not user.is_active:
            return Response({'message': 'Your account is not verified, verify it first.'}, status=status.HTTP_400_BAD_REQUEST)

        if not authenticate(username=serializer.data['email'], password=serializer.data['password']):
            return Response({'message': 'Your password did not match with an entered email.'}, status=status.HTTP_400_BAD_REQUEST)


        token, created = Token.objects.get_or_create(user=user)        
        return Response({'token': token.key, "userData": user_serializer.data})


class LogoutViewSet(viewsets.ViewSet):
    
    def create(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        return Response({'success': 'Successfully logged out.'}, status=status.HTTP_200_OK)


# View set for the registration OTP verification

class RegistrationOtpVerificationViewSet(viewsets.ViewSet):
    
    def create(self, request):
        auth_otp_serializer = RegisterOtpSerializer(data=request.data)
        auth_otp_serializer.is_valid(raise_exception=True)
        user_queryset = User.objects.all()
        user = get_object_or_404(user_queryset, email=auth_otp_serializer.data['email'])
        otp_queryset = RegisterUserOtp.objects.all()
        otp = get_object_or_404(otp_queryset, otp=auth_otp_serializer.data['otp'], user=user)

        user.is_active = True
        user.save()
        otp.delete()
        
        serializer = UserSerializer(user)
        return Response(serializer.data)
        

# View set for the forgot password 

class ForgotPasswordViewSet(viewsets.ViewSet):
    
    def create(self, request):
        forget_password_serializer = ForgotPasswordSerializer(data=request.data)
        forget_password_serializer.is_valid(raise_exception=True)

        user_queryset = User.objects.all()
        user = get_object_or_404(user_queryset, email=forget_password_serializer.data['email'])

        # Let's create otp for the forgot password
        otp = generate_otp() 
        send_auth_mail("Forgot password OTP", f" Hello {user.name}, your forgot password OTP is {otp}", [user.email])
        ForgotPasswordOtp.objects.filter(user=user).delete()

        otp_serializer = ForgotPasswordOtpSerializer(data={'user':user.id, 'otp': otp})
        otp_serializer.is_valid(raise_exception=True)        
        otp_serializer.save()
        return Response({'message': 'New OTP was created for the forgot password.'}, status=status.HTTP_201_CREATED)


# View set for the verify forgot password

class ForgotPasswordOtpVerificationAndResetPasswordViewSet(viewsets.ViewSet):
    
    def create(self, request):
        opt_verification_serializer = ForgotPasswordOtpVerifyAndResetPasswordSerializer(data=request.data)
        opt_verification_serializer.is_valid(raise_exception=True)

        user_queryset = User.objects.all()
        user = get_object_or_404(user_queryset, email=opt_verification_serializer.data['email'])

        forgot_password_otp_queryset = ForgotPasswordOtp.objects.all()
        forgot_password_otp = get_object_or_404(forgot_password_otp_queryset, user=user, otp=opt_verification_serializer.data['otp'])
        forgot_password_otp.delete()

        user.set_password(opt_verification_serializer.data['password'])

        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)


# Reset password view set

class ResetPasswordViewSet(viewsets.ViewSet):
    def partial_update(self, request, pk=None):
        reset_password_serializer = ResetPasswordSerializer(data=request.data)
        reset_password_serializer.is_valid(raise_exception=True)

        user_queryset = User.objects.all()
        user = get_object_or_404(user_queryset, pk=pk)

        if not authenticate(username=user.email, password=reset_password_serializer.data['old_password']):
            return Response({'message': 'Your old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(reset_password_serializer.data['new_password'])
        user.save()
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)