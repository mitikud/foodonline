from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .registration_form import UserForm
from .models import User, UserProfile
from vendor.vendor_registration_form import VendorForm

# Create your views here.

def registerUser(request):
    # return HttpResponse(" this is user registeeration")
    if request.method == 'POST':
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
    # return HttpResponse("Vendor has been registered successfully")
    if request.method == 'POST':
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
