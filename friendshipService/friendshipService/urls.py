from django.contrib import admin
from django.urls import path, include
# from friendshipService.apps.friendshipApp.urls import urlpatterns as imported
# does not work

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('friendshipApp.urls')),
]
