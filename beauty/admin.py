from django.contrib import admin
from .models import Category, Service, Master, Client, Appointment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'duration_minutes', 'category')
    list_filter = ('category',)
    search_fields = ('name',)
    list_editable = ('price', 'duration_minutes')


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'specialization')
    filter_horizontal = ('services',)
    search_fields = ('name',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'registered_at')
    search_fields = ('name', 'phone')
    readonly_fields = ('registered_at',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'service', 'master', 'start_time', 'status', 'created_at')
    list_filter = ('status', 'start_time', 'master')
    search_fields = ('client__name', 'client__phone')
    readonly_fields = ('created_at',)
    list_editable = ('status',)