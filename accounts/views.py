from django.http import HttpResponse
from django.shortcuts import redirect, render

from .registration_form import UserForm
from .models import User

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
