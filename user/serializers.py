from rest_framework import serializers
from .models import User, RegisterUserOtp, ForgotPasswordOtp
from .validators import validate_otp_number


class UserSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}, 'email': {'error_messages': {"required": "Email is required.", "invalid":"Invalid email address."}}}
    
   
    def create(self, validated_data):
        validated_data.pop('is_active', None)
        validated_data.pop('last_login', None)
        validated_data.pop('is_staff', None)
        validated_data.pop('date_joined', None)
        validated_data.pop('updated_at', None)
        validated_data.pop('user_permissions', None)
        validated_data.pop('groups', None)
 
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user;       

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.name = validated_data.get('name', instance.name)
        instance.location = validated_data.get('location', instance.location)
        instance.profile_image = validated_data.get('profile_image', instance.profile_image)
        instance.save()
        return instance


class RegisterUserOtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterUserOtp
        fields = '__all__'


class ForgotPasswordOtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForgotPasswordOtp
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)


class RegisterOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6, validators=[validate_otp_number])
 

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ForgotPasswordOtpVerifyAndResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6, validators=[validate_otp_number])
    password = serializers.CharField(max_length=100)


class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=100)
    new_password = serializers.CharField(max_length=100)
