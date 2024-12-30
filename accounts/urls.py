from django.urls import include, path

from . import views


urlpatterns = [
    path('', views.myAccount, name='myAccount'),
    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerVendor/', views.registerVendor, name='registerVendor'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('vendordashboard/', views.vendordashboard, name='vendordashboard'),
    path('customerdashboard/', views.customerdashboard, name='customerdashboard'),

    
    path('myAccount/', views.myAccount, name='myAccount'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    
    path('reset_password/', views.reset_password, name='reset_password'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),

    path('vendor/', include('vendor.urls')),
    # path('customer/', include('customer.urls')),
]