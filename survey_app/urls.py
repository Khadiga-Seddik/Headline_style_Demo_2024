from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    # path('start_page/', views.start_page, name='start_page'),
    path('personal_info/', views.personal_info, name='personal_info'),
    path('front_page/', views.front_page, name='front_page'),
    path('read_later/', views.read_later, name='read_later'),
    path('end_page/', views.end_page, name='end_page'),
    path('error_page/', views.error_page, name='error_page'),
    path('remove_read_later', views.remove_read_later, name='remove_read_later'),
]