
from django.urls import path
from . import views
from accounts import views as Accountviews

urlpatterns = [
    path('', Accountviews.customerdashboard, name='customer'),
    path('profile/', views.customer_profile, name='customer_profile'),
    # path('profile/', views.customer_profile, name='customer_profile'),
]