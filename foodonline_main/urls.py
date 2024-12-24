
from django.contrib import admin
from django.urls import include, path
from . import views
from marketplace import views  as CartView
from django.conf import settings
from django.conf.urls.static import static

from marketplace import views as Marketplaceviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('marketplace/', include('marketplace.urls')),
    
    #cart
    path('cart/', CartView.cart, name='cart'),

    #Search
    path('search/', Marketplaceviews.search, name='search'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
