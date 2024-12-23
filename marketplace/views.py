from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.db.models import Prefetch
from marketplace.context_processor import get_cart_counter
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
  
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'cart_items': cart_items,
        'vendor': vendor,
        'categories': categories
        }
    return render(request, 'marketplace/vendor_detail.html', context)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        if is_ajax(request=request):
            #check if the food item exist
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                #check if the user has already added the food item to the cart
                try:
                    chkcart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    #increase the cart quantity
                    chkcart.quantity+=1
                    chkcart.save()
                    # return JsonResponse({'status':'success','message':'increased the card quantity'})
                    return JsonResponse({'status':'success','message':'increased the card quantity', 'cart_counter': get_cart_counter(request),'qty':chkcart.quantity})
                except:
                    chkcart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status':'success','message':'Added the food item to the cart','cart_counter': get_cart_counter(request),'qty':chkcart.quantity})
            except :
                return JsonResponse({'status':'failed','message':'this food does not exist'})
            
        else:
            return JsonResponse({'status':'failed','message':'invalied response'})
    else:
        return JsonResponse({'status':'login required','message':'please login to continue'})

def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        if is_ajax(request=request):
            #check if the food item exist
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                #check if the user has already added the food item to the cart
                try:
                    chkcart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    #decrease the cart quantity
                    if chkcart.quantity > 1:
                        chkcart.quantity-= 1
                        chkcart.save()
                    else:
                        chkcart.delete()
                        chkcart.quantity = 0

                    # return JsonResponse({'status':'success','message':'increased the card quantity'})
                    return JsonResponse({'status':'success','message':'decreased the card quantity', 'cart_counter': get_cart_counter(request),'qty':chkcart.quantity})
                except:
                   
                    return JsonResponse({'status':'failed','message':'you do not have this item in your cart'})
            except :
                return JsonResponse({'status':'failed','message':'this food does not exist'})
            
        else:
            return JsonResponse({'status':'failed','message':'invalied response'})
    else:
        return JsonResponse({'status':'login required','message':'please login to continue'})

# @login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'cart/cart.html', context)

def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if is_ajax(request=request):
            try:
                #check if cart item exists
                cart_item = Cart.objects.get(user=request.user,id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status':'success','message':'cart item deleted successfully','cart_counter': get_cart_counter(request)})
            except:
                return JsonResponse({'status':'failed','message':'Cart item not found'})

        else:
            return JsonResponse({'status':'failed','message':'invalied response', 'cart_counter': get_cart_counter(request)})