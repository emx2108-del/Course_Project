from django.urls import path
from . import views

app_name = 'beauty'

urlpatterns = [
    path('', views.index, name='index'),
    path('service/<int:service_id>/', views.service_detail, name='service_detail'),
    path('masters/', views.masters_list, name='masters_list'),
    path('master/<int:master_id>/', views.master_detail, name='master_detail'),
    path('appointment/create/', views.appointment_create, name='appointment_create'),
    path('appointment/success/', views.appointment_success, name='appointment_success'),
    path('my-appointments/', views.my_appointments, name='my_appointments'),
]