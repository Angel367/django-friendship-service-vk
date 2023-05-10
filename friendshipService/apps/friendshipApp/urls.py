from django.urls import path
from .views import view_friends

urlpatterns = [
    path('friends/<int:user_id>/', view_friends, name='view_friends'),
]
