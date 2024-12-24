from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from .vendor_registration_form import VendorForm, OpeningHoursForm
from accounts.registration_form import UserProfileForm
from accounts.models import UserProfile
from .models import Vendor, OpeningHours
from menue.models import Category, FoodItem
from menue.menue_form import CategoryForm, FoodItemForm

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

@login_required(login_url='login')
@user_passes_test(check_vendor_role)
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
@login_required(login_url='login')
@user_passes_test(check_vendor_role)
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
@login_required(login_url='login')
@user_passes_test(check_vendor_role)
def delete_category(request, pk=None):
    # return render(request, 'vendor/edit_category.html')
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category has been deleted successfully')
    return redirect('menue_builder')

@login_required(login_url='login')
@user_passes_test(check_vendor_role)
def add_food_item(request):
    if request.method == 'POST':
       form = FoodItemForm(request.POST, request.FILES) 
       if form.is_valid():
           food_title = form.cleaned_data['food_title']
           food = form.save(commit=False)
           vendor = Vendor.objects.get(user=request.user)
           food.vendor = vendor
           food.slug = slugify(food_title) #change to slug example sea food to sea_food
           form.save()
           messages.success(request, 'food item added successfully')
           return redirect('foodItems_by_category', food.category.id)
       else:
           print(form.errors)
    else:
        form = FoodItemForm()
        vendor = Vendor.objects.get(user=request.user)
        form.fields['category'].queryset = Category.objects.filter(vendor=vendor)
    context = {
       'form': form
    }
    return render(request, 'vendor/add_food_item.html', context)

@login_required(login_url='login')
@user_passes_test(check_vendor_role)
def edit_food_item(request, pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
       form = FoodItemForm(request.POST, instance=food) 
       if form.is_valid():
           food_title = form.cleaned_data['food_title']
           food = form.save(commit=False)
           vendor = Vendor.objects.get(user=request.user)
           food.vendor = vendor
           food.slug = slugify(food_title) #change to slug example sea food to sea_food
           form.save()
           messages.success(request, 'food item updated successfully')
           return redirect('foodItems_by_category', food.category.id)
       else:
           print(form.errors)
    else :
        form = FoodItemForm(instance=food)
        vendor = Vendor.objects.get(user=request.user)
        form.fields['category'].queryset = Category.objects.filter(vendor=vendor)
    context = {
        'form': form,
        'food': food,
        'category': food.category
    }
    return render(request, 'vendor/edit_food_item.html', context)

@login_required(login_url='login')
@user_passes_test(check_vendor_role)
def delete_food_item(request, pk=None):
    # return render(request, 'vendor/edit_category.html')
    food = get_object_or_404(FoodItem, pk=pk)
    food.delete()
    messages.success(request, 'Food item has been deleted successfully')
    return redirect('foodItems_by_category', food.category.id)

def opening_hours(request):
    vendor =  Vendor.objects.get(user=request.user)
    opening_hour = OpeningHours.objects.filter(vendor=vendor)
    print(opening_hour)
    from_hr = OpeningHoursForm()
    context = {
        'from_hr': from_hr,
        'opening_hour': opening_hour
    }
    return render(request, 'vendor/opening_hours.html', context)