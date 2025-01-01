# models.py

from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField(help_text="Duration in minutes")
    photo = models.ImageField(upload_to='service/', null=True, blank=True)  # Service photo

    def __str__(self):
        return self.name
    
class Employee(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    working_start_time = models.TimeField(default='09:00')
    working_end_time = models.TimeField(default='17:00')
    photo = models.ImageField(upload_to='employees/', null=True, blank=True, default='path/to/default/photo.jpg')

    def __str__(self):
        return self.name


class Appointment(models.Model):
    employee = models.ForeignKey(Employee, related_name='appointments', on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=15)
    appointment_time = models.DateTimeField()
    status = models.CharField(max_length=20, default='Scheduled', choices=[('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Canceled', 'Canceled')])
    services = models.ManyToManyField(Service, related_name='appointments')  # Link to Service model

    def __str__(self):
        return f"Appointment with {self.employee.name} at {self.appointment_time}"
