from django.urls import include, path

from . import views
from accounts import views as AccountViews

urlpatterns = [
    path('', AccountViews.vendordashboard,name='vendor'),
    path('vendor_profile/', views.vendor_profile, name='vendor_profile'),
    path('menue_builder/', views.menueBulder, name='menue_builder'),
    path('menue_builder/category/<int:pk>/', views.foodItems_by_category, name='foodItems_by_category'),

    # Category CRUD
    path('menue_builder/category/add/', views.add_category, name='add_category'),
    path('menue_builder/category/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('menue_builder/category/delete/<int:pk>/', views.delete_category, name='delete_category'),

    # Food item CRUD
    path('menue_builder/food/add/', views.add_food_item, name='add_food_item'),
    path('menue_builder/food/edit/<int:pk>/', views.edit_food_item, name='edit_food_item'),
    path('menue_builder/food/delete/<int:pk>/', views.delete_food_item, name='delete_food_item'),
    
    #opening hours
    path('opening_hours/', views.opening_hours, name='opening_hours'),
    path('opening_hours/add/', views.add_opening_hours, name='add_opening_hours'),
    path('opening_hours/remove/<int:pk>/', views.remove_opening_hour, name='remove_opening_hour'),
    

]