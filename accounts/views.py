from django.contrib import messages, auth
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_decode
from accounts.util import detect_redirect, send_verification_email
from django.contrib.auth.tokens import default_token_generator

from .registration_form import UserForm
from .models import User, UserProfile
from vendor.models import Vendor
from vendor.vendor_registration_form import VendorForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt

from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.core.mail import send_mail 
from .util import send_password_reset_email
# Create your views here.

#Restrict a vendor from accessing the user dashboard
def check_vendor_role(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied
#Restrict a user from accessing the vendor's dashboard
def check_user_role(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already logged in")
        return redirect('myAccount')
    # return HttpResponse(" this is user registeeration")
    elif request.method == 'POST':
        # print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            # method 1 create the user using the form

            # password = form.cleaned_data['password'] #get the passsword
            # user = form.save(commit=False) # the user is ready to be saved but not saved yet
            # user.set_password(password) # hash the password
            # user.role = User.CUSTOMER
            # user.save() # the user is  saved in db

            # method 2 create the user using create_user method from the models.py
            first_name = form.cleaned_data['first_name'] #get the first_name
            last_name = form.cleaned_data['last_name'] #get the last_name
            username = form.cleaned_data['username'] #get the username
            email = form.cleaned_data['email'] #get the email
            password = form.cleaned_data['password'] #get the password
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email, 
                password=password)
            user.role = User.CUSTOMER
          
            user.save()
            
            # #  send verification email
            # try:
            #     send_verification_email(request, user)
            #     messages.success(request, "Your account has been registered successfully! Please check your email to verify your account.")
            # except Exception as e:
            #     messages.warning(request, f"Unable to send verification email. Please try again later. Error: {e}")
            messages.info(request,"Your user has been register successfully!")
            return redirect('registerUser')
        else:
            print("Invalied form!")
            print(form.non_field_errors)
            print(form.errors)
    else:
        form = UserForm()
    context = {
        'form': form,
   
    }
    return render(request,'accounts/register.html',context)


def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already logged in")
        return redirect('myAccount')
    # return HttpResponse("Vendor has been registered successfully")
    elif request.method == 'POST':
        form = UserForm(request.POST)
        vendor_form = VendorForm(request.POST, request.FILES)

        if vendor_form.is_valid() and form.is_valid():
            first_name = form.cleaned_data['first_name'] #get the first_name
            last_name = form.cleaned_data['last_name'] #get the last_name
            username = form.cleaned_data['username'] #get the username
            email = form.cleaned_data['email'] #get the email
            password = form.cleaned_data['password'] #get the password
            user = User.objects.create_user(
                first_name=first_name, 
                last_name=last_name, 
                username=username,
                email=email, 
                password=password)
            user.role = User.VENDOR
            user.save()
             #send verification email
            # send_verification_email(request,user)
             # Create or get UserProfile
            user_profile, created = UserProfile.objects.get_or_create(user=user)

            vendor = vendor_form.save(commit=False)
            vendor.user = user
            # user_profile = UserProfile.objects.get(user= user)
            # user.user_profile = user_profile
            vendor.user_profile = user_profile
            vendor.save()
            messages.info(request,"Your account has been register successfully!, please waite for approval")
            return redirect('registerVendor')
        else:
            print("Invalid form")
            print(form.errors)
            print(vendor_form.errors)
    else:
        form = UserForm()
        vendor_form = VendorForm()

    context = {
        'form': form,
        'vendor_form': vendor_form,
    }
    return render(request, 'accounts/registervendor.html', context)
def login(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already logged in")
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # check if email and password exist and return the user
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request, "Your are now logedd in successfully")
            return redirect('myAccount')
        else:
            messages.error(request, "Invalied credential")
            return redirect('login')

    

    return render(request, 'accounts/login.html')

def activate(request, uidb64, token):
    # activate the user by setiining is_active to true
    try:
        uid=urlsafe_base64_decode(uidb64)
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError,user.DoesNotExist):
        user = None
        # print(f"Activation error: {e}")
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations! Your account is activated!")
        return redirect('myAccount')
    else:
        messages.error(request,'Invalid activation link.')
        return redirect('myAccount')


def logout(request):
   auth.logout(request)
   messages.info(request, "you are logged out successfully")
   
   return redirect('login')

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detect_redirect(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_user_role)
def customerdashboard(request):
    
    return render(request, 'accounts/customerdashboard.html')
@login_required(login_url='login')
@user_passes_test(check_vendor_role)
def vendordashboard(request):
    # vendor = Vendor.objects.get(user=request.user)
    # context = {
    #     'vendor': vendor
    # }
    # return render(request, 'accounts/vendordashboard.html', context)
    return render(request, 'accounts/vendordashboard.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__iexact=email)
            send_password_reset_email(request,user)
            messages.success(request, "password reset link has been send to your email address")
            return redirect('login')
        else:
            messages.error(request, "the account doesn't exists")
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')
def reset_password(request):
    return render(request, 'accounts/rest_password.html')
def reset_password_validate(request, uiddb64, token):
    return 

