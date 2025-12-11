from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

def home(request):
    return render(request, "home.html")

urlpatterns = [
    path('admin/', admin.site.urls),

    # home page
    path("", home, name="home"),

    # accounts
    path("", include("accounts.urls", namespace="accounts")),

    # restaurants
    path("restaurants/", include("restaurants.urls", namespace="restaurants")),

    # browser reload
    path("django-browser-reload/", include("django_browser_reload.urls")),

    # admin panel
    # path("adminpanel/", include("accounts.urls", namespace="accounts")),
    
    # chats
    path('chats/', include('chats.urls')),

    # drivers
    path('drivers/', include('drivers.urls', namespace='drivers')), # PASTIKAN ADA INI

   
]
