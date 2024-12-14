from django.contrib import messages, auth
from django.http import HttpResponse
from django.shortcuts import redirect, render

from accounts.util import detect_redirect

from .registration_form import UserForm
from .models import User, UserProfile
from vendor.vendor_registration_form import VendorForm
from django.contrib.auth.decorators import login_required, user_passes_test

from django.core.exceptions import PermissionDenied
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
            last_name = form.cleaned_data['first_name'] #get the last_name
            username = form.cleaned_data['username'] #get the username
            email = form.cleaned_data['email'] #get the email
            password = form.cleaned_data['password'] #get the password
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()
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
            last_name = form.cleaned_data['first_name'] #get the last_name
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
             # Create or get UserProfile
            user_profile, created = UserProfile.objects.get_or_create(user=user)

            vendor = vendor_form.save(commit=False)
            # vendor.user = user
            # user_profile = UserProfile.objects.get(user= user)
            user.user_profile = user_profile
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
    return render(request, 'accounts/vendordashboard.html')