from django import forms
from .models import Appointment, Employee, Service
from django.core.exceptions import ValidationError
from datetime import timedelta

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'phone', 'email', 'working_start_time', 'working_end_time', 'photo']

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'price', 'duration', 'photo']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['employee', 'customer_name', 'customer_phone', 'appointment_time', 'services']
        widgets = {
            'appointment_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_appointment_time(self):
        appointment_time = self.cleaned_data['appointment_time']
        employee = self.cleaned_data['employee']

        appointment_time = appointment_time.replace(minute=0, second=0, microsecond=0)

        if not (employee.working_start_time <= appointment_time.time() <= employee.working_end_time):
            raise ValidationError(f"The appointment time must be between {employee.working_start_time} and {employee.working_end_time}.")

        existing_appointment = Appointment.objects.filter(
            employee=employee,
            appointment_time=appointment_time
        ).exists()

        if existing_appointment:
            raise ValidationError("This time slot is already booked.")

        return appointment_time


