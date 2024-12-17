from django.urls import include, path

from . import views
from accounts import views as AccountViews

urlpatterns = [
    path('', AccountViews.vendordashboard,name='vendor'),
    path('vendor_profile/', views.vendor_profile, name='vendor_profile'),

]