from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from .vendor_registration_form import VendorForm
from accounts.registration_form import UserProfileForm
from accounts.models import UserProfile
from .models import Vendor
from menue.models import Category, FoodItem
from menue.menue_form import CategoryForm

from django.contrib import messages
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_vendor_role
# Create your views here.
@login_required(login_url='login')
@user_passes_test(check_vendor_role)
def vendor_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST,request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST,request.FILES,instance=vendor)
        if vendor_form.is_valid() and profile_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request,"settings updated successfully")
            return redirect('vendor_profile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)
    context = {
        "profile_form":profile_form,
        "vendor_form":vendor_form,
        "profile":profile,
        "vendor":vendor,

    }
    return render(request, 'vendor/vendor_profile.html', context)

@login_required(login_url='login')
@user_passes_test(check_vendor_role)
def menueBulder(request):
    vendor = Vendor.objects.get(user=request.user)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    context = {
        'categories': categories,
    }
    return render(request, 'vendor/menue_bulder.html', context)

@login_required(login_url='login')
@user_passes_test(check_vendor_role)
def foodItems_by_category(request, pk=None):
    try:
        # Ensure the current user is associated with a vendor
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        return HttpResponseForbidden("You are not authorized to access this page.")

    # Fetch the category or return a 404 error if it does not exist
    category = get_object_or_404(Category, pk=pk)

    # Fetch food items for the given category and vendor
    foodItems = FoodItem.objects.filter(vendor=vendor, category=category)
    
    # Pass the data to the template
    context = {
        
        'category': category,
        'fooditems': foodItems,
    }

    return render(request, 'vendor/food_items_by_category.html', context)

def add_category(request):
    if request.method == 'POST':
       form = CategoryForm(request.POST) 
       if form.is_valid():
           category_name = form.cleaned_data['category_name']
           category = form.save(commit=False)
           vendor = Vendor.objects.get(user=request.user)
           category.vendor = vendor
           category.slug = slugify(category_name) #change to slug example sea food to sea_food
           form.save()
           messages.success(request, 'Category added successfully')
           return redirect('menue_builder')
       else:
           print(form.errors)
    else :
        form = CategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'vendor/add_category.html', context)
def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
       form = CategoryForm(request.POST, instance=category) 
       if form.is_valid():
           category_name = form.cleaned_data['category_name']
           category = form.save(commit=False)
           vendor = Vendor.objects.get(user=request.user)
           category.vendor = vendor
           category.slug = slugify(category_name) #change to slug example sea food to sea_food
           form.save()
           messages.success(request, 'Category updated successfully')
           return redirect('menue_builder')
       else:
           print(form.errors)
    else :
        form = CategoryForm(instance=category)
    context = {
        'form': form,
        'category': category
    }
    return render(request, 'vendor/edit_category.html', context)
def delete_category(request, pk=None):
    # return render(request, 'vendor/edit_category.html')
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category has been deleted successfully')
    return redirect('menue_builder')


def add_food_item(request):
   
    return render(request, 'vendor/add_food_item.html')