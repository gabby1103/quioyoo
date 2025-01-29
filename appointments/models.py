# models.py

from django.db import models
from django.contrib.auth.models import User


    
class Employee(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    working_start_time = models.TimeField(default='09:00')
    working_end_time = models.TimeField(default='17:00')
    photo = models.ImageField(upload_to='employees/', null=True, blank=True, default='path/to/default/photo.jpg')

    def __str__(self):
        return self.name

class NailDesign(models.Model):
    name = models.CharField(max_length=255)  # Name of the nail design
    description = models.TextField(null=True, blank=True)  # Description of the design
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the design
    photo = models.ImageField(upload_to='nail_designs/', null=True, blank=True, default='path/to/default/photo.jpg')  # Image of the design

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=255)  # Name of the service
    description = models.TextField(null=True, blank=True)  # Description of the service
    photo = models.ImageField(upload_to='services/', null=True, blank=True, default='path/to/default/photo.jpg')  # Service image
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the service

    def __str__(self):
        return self.name


class Appointment(models.Model):
    employee = models.ForeignKey(Employee, related_name='appointments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='appointments', on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=15)
    appointment_time = models.DateTimeField()
    status = models.CharField(max_length=20, default='Scheduled', choices=[('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Canceled', 'Canceled')])

    nail_design = models.ForeignKey(NailDesign, null=True, blank=True, on_delete=models.SET_NULL)
    services = models.ManyToManyField(Service, blank=True)  # Use ManyToManyField for services

    def __str__(self):
        return f"Appointment with {self.employee.name} at {self.appointment_time}"

    
class Inventory(models.Model):
    name = models.CharField(max_length=255)  # Product or supply name
    description = models.TextField(null=True, blank=True)  # Product details or usage description
    quantity_in_stock = models.PositiveIntegerField()  # Current stock level
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)  # Price per unit of the product

    def __str__(self):
        return self.name
