from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin panel URL
    path('admin/', admin.site.urls),
    
    # Include URLs from the 'ecard' app
    path('', include('ecard.urls')),  # Include ecard app's URLs
]
