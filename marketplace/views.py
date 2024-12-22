from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.db.models import Prefetch
from vendor.models import Vendor
from menue.models import Category, FoodItem
from .models import Cart

# Create your views here.

def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count =  vendors.count()
    context  = {
        'vendors': vendors,
        'vendor_count': vendor_count
    }
    return render(request, 'marketplace/listing.html', context)

def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    #prefech is used to reverse look up ie from category to find the fooditem 
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset=FoodItem.objects.filter(is_available=True)
        )
    )
  
    context = {
        'vendor': vendor,
        'categories': categories
        }
    return render(request, 'marketplace/vendor_detail.html', context)


def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        if request.is_ajax():
            #check if the food item exist
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                #check if the user has already added the food item to the cart
                try:
                    chkcart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    #increase the cart quantity
                    chkcart.quantity+=1
                    chkcart.save()
                    return JsonResponse({'status':'success','message':'increased the card quantity'})
                except:
                    chkcart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status':'success','message':'Added the food item to the cart'})
            except :
                return JsonResponse({'status':'failed','message':'this food does not exist'})
            
        else:
            return JsonResponse({'status':'failed','message':'invalied response'})
    else:
        return JsonResponse({'status':'failed','message':'please login to continue'})

