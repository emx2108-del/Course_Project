from django import forms
from django.utils import timezone
from .models import Appointment, Master, Service


class AppointmentForm(forms.ModelForm):
    client_name = forms.CharField(
        max_length=100,
        label='Ваше имя',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иван Иванов'})
    )
    client_phone = forms.CharField(
        max_length=20,
        label='Номер телефона',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (999) 123-45-67'})
    )
    
    class Meta:
        model = Appointment
        fields = ['service', 'master', 'start_time', 'comment']
        widgets = {
            'service': forms.Select(attrs={'class': 'form-control'}),
            'master': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Пожелания к визиту...'}),
        }
        labels = {
            'service': 'Услуга',
            'master': 'Мастер',
            'start_time': 'Дата и время',
            'comment': 'Комментарий',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['master'].queryset = Master.objects.all()
        self.fields['service'].queryset = Service.objects.all()
    
    def clean_start_time(self):
        start_time = self.cleaned_data.get('start_time')
        if start_time and start_time < timezone.now():
            raise forms.ValidationError('Нельзя записаться на прошедшее время')
        return start_time