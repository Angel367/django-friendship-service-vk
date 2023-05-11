from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('friends/', friends_view, name='view_friends'),    # Друзья пользователя
    path('add_friend/', add_friend, name='add_friend'),     # Добавить друга
    path('users/', user_list, name='user_list'),            # Все пользователи
    path('index', index_view, name='index_view'),           # Главная страница
    path('received_requests/', received_requests_view, name='received_requests_view'),  # Входящие заявки
    path('sent_requests/', sent_requests_view, name='sent_requests_view'),  # Исходящие заявки
    path('all_requests/', all_requests_view, name='all_requests_view'),     # Все заявки
    path('', index_view, name='index_view'),    # Главная страница
    re_path(r'^register/$', register_view, name='register_view'),   # Регистрация
    path('logout', auth_views.LogoutView.as_view(next_page='/'), name='logout'),    # Де аутентификация
    re_path(r'^login/$', auth_views.LoginView.as_view(next_page='/'), name='login') # Авторизация
]
