from django.conf import settings
from django.core.mail import send_mail
import math, random


def send_auth_mail(subject, message, recipient_list):
    email_from = settings.EMAIL_HOST_USER

    send_mail(
        subject, 
        message,
        email_from,
        recipient_list,
        recipient_list
    ) 


def generate_otp():
    digits = "0123456789"
    OTP = ""
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP   

   
