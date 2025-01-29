from django import forms
from .models import Appointment, Employee, Inventory, NailDesign, Service
from django.core.exceptions import ValidationError
from datetime import timedelta


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'phone', 'email', 'working_start_time', 'working_end_time', 'photo']


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'photo', 'price']

    
class AppointmentForm(forms.ModelForm):
    # Add a NailDesign field (optional)
    nail_design = forms.ModelChoiceField(
        queryset=NailDesign.objects.all(), 
        required=False,  # Make it optional
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Nail Design"
    )
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # You can customize the widget here to make it look like a dropdown
        required=True
    )

    class Meta:
        model = Appointment
        fields = ['employee', 'customer_name', 'customer_phone', 'appointment_time', 'nail_design', 'services']  # Include services
        widgets = {
            'appointment_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_appointment_time(self):
        appointment_time = self.cleaned_data['appointment_time']
        employee = self.cleaned_data['employee']

        # Normalize the time to avoid minute/second discrepancies
        appointment_time = appointment_time.replace(minute=0, second=0, microsecond=0)

        # Check if the appointment is within the employee's working hours
        if not (employee.working_start_time <= appointment_time.time() <= employee.working_end_time):
            raise ValidationError(f"The appointment time must be between {employee.working_start_time} and {employee.working_end_time}.")

        # Check for existing appointments at the same time slot
        existing_appointment = Appointment.objects.filter(
            employee=employee,
            appointment_time=appointment_time
        ).exclude(status='Canceled')  # Exclude canceled appointments from this check

        if existing_appointment.exists():
            raise ValidationError("This time slot is already booked by another user.")

        return appointment_time


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['name', 'description', 'quantity_in_stock', 'price_per_unit']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
class NailDesignForm(forms.ModelForm):
    class Meta:
        model = NailDesign
        fields = ['name', 'description', 'price', 'photo']