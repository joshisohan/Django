from django.urls import path
from basic_app import views

app_name = 'basic_app'

urlpatterns=[
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
    path('special_page/', views.special_page, name='special_page'),
]