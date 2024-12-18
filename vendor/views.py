from django.shortcuts import get_object_or_404, redirect, render
from .vendor_registration_form import VendorForm
from accounts.registration_form import UserProfileForm
from accounts.models import UserProfile
from .models import Vendor
from django.contrib import messages

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