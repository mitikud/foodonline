from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.conf import settings
def detect_redirect(user):
    if user.role == 1:
        redirectUrl = 'vendordashboard'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = 'customerdashboard'
        return redirectUrl
    elif user.role == None and user.is_superuser:
        redirectUrl = '/admin'
        return redirectUrl
    
#Verification email
# def send_verification_email(request,user):
#     from_email = settings.DEFAULT_FROM_EMAIL
#     current_site = get_current_site(request)
#     mail_subject = "Please activate your account. "
#     message = render_to_string("accounts/emails/account_verification_email.html", {
#         "user": user,
#         "domain": current_site,
#         "uid": urlsafe_base64_encode(force_bytes(user.pk)),
#         "token": default_token_generator.make_token(user),

#     })
#     to_email= user.email
#     mail = EmailMessage(mail_subject, message,from_email, to=[to_email])
#     try:
#         mail.send()
#     except Exception as e:
#     # Log the error and inform the user/admin
#         print(f"Email sending failed: {e}")
# def send_password_reset_email(request,user):
#     from_email = settings.DEFAULT_FROM_EMAIL
#     current_site = get_current_site(request)
#     mail_subject = "Reset your password"
#     message = render_to_string("accounts/emails/send_password_reset_email.html", {
#         "user": user,
#         "domain": current_site,
#         "uid": urlsafe_base64_encode(force_bytes(user.pk)),
#         "token": default_token_generator.make_token(user),

#     })
#     to_email= user.email
#     mail = EmailMessage(mail_subject, message,from_email, to=[to_email])
#     mail.send()

def send_password_reset_email(request, user):
    
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    domain = request.get_host()
    subject = "Reset Your Password"
    message = render_to_string('accounts/emails/send_password_reset_email.html', {
        'user': user,
        'domain': domain,
        'uid': uid,
        'token': token,
    })

    send_mail(subject, message, 'no-reply@example.com', [user.email])
    
def send_verification_email(request, user):
   
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    domain = request.get_host()
    subject = "Activate Your Account"
    message = render_to_string('accounts/emails/activation_email.html', {
        'user': user,
        'domain': domain,
        'uid': uid,
        'token': token,
    })
    to_email= user.email

    send_mail(subject, message, 'no-reply@example.com',  [user.email])

