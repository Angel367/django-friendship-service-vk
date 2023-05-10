from django.contrib import admin
from django.urls import path
# from friendshipService.apps.friendshipApp.urls import urlpatterns as imported
# does not work

urlpatterns = [
    path('admin/', admin.site.urls),
] + imported
