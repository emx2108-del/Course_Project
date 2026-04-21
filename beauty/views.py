from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Service, Master, Appointment, Client
from .forms import AppointmentForm


def index(request):
    services = Service.objects.all().select_related('category')
    masters = Master.objects.all()[:3]
    return render(request, 'beauty/index.html', {
        'services': services,
        'masters': masters,
        'title': 'Главная'
    })


def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    masters = service.masters.all()
    return render(request, 'beauty/service_detail.html', {
        'service': service,
        'masters': masters,
        'title': service.name
    })


def masters_list(request):
    masters = Master.objects.all().prefetch_related('services')
    return render(request, 'beauty/masters.html', {
        'masters': masters,
        'title': 'Наши мастера'
    })


def master_detail(request, master_id):
    master = get_object_or_404(Master, id=master_id)
    return render(request, 'beauty/master_detail.html', {
        'master': master,
        'title': master.name
    })


def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            
            phone = form.cleaned_data.get('client_phone')
            name = form.cleaned_data.get('client_name')
            
            if phone:
                client, created = Client.objects.get_or_create(
                    phone=phone,
                    defaults={'name': name or 'Гость'}
                )
                if not created and name:
                    client.name = name
                    client.save()
                appointment.client = client
            
            appointment.save()
            messages.success(request, 'Вы успешно записаны! Мы ждем вас.')
            return redirect('beauty:appointment_success')
    else:
        form = AppointmentForm()
    
    return render(request, 'beauty/appointment_create.html', {
        'form': form,
        'title': 'Записаться'
    })


def appointment_success(request):
    return render(request, 'beauty/appointment_success.html', {
        'title': 'Запись оформлена'
    })


def my_appointments(request):
    appointments = None
    phone = None
    
    if request.method == 'POST':
        phone = request.POST.get('phone')
        if phone:
            try:
                client = Client.objects.get(phone=phone)
                appointments = client.appointments.all().select_related('service', 'master')
                messages.info(request, f'Найдено записей: {appointments.count()}')
            except Client.DoesNotExist:
                messages.warning(request, 'Клиент с таким телефоном не найден')
    
    return render(request, 'beauty/my_appointments.html', {
        'appointments': appointments,
        'phone': phone,
        'title': 'Мои записи'
    })