from django.core.exceptions import ValidationError


def validate_phone_number(value):
    if not value.isnumeric:
        raise ValidationError(
            'Phone number can not be string.',
            params={'value': value},
        )
    
    if not len(value) == 10:
        raise ValidationError('Phone number must be 10 digit numbers.')


def validate_otp_number(value):
    if not value.isnumeric:
        raise ValidationError(
            'OTP can not be string.',
            params={'value': value},
        )
    
    if not len(value) == 6:
        raise ValidationError('OTP must be 6 digit numbers.')
        