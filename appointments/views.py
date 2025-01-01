from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Employee, Appointment, Service
from .forms import AppointmentForm, EmployeeForm, ServiceForm

def index(request):
    return render(request, 'appointments/index.html')
    
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment_time = form.cleaned_data['appointment_time']
            employee = form.cleaned_data['employee']
            existing_appointment = Appointment.objects.filter(
                employee=employee,
                appointment_time=appointment_time
            ).exclude(status='Canceled')
            if existing_appointment.exists():
                form.add_error('appointment_time', "This time slot is already booked.")
            else:
                form.save()
                return redirect('appointments:appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'appointments/book_appointment.html', {'form': form})

def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointments:appointment_list')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'appointments/edit_appointment.html', {'form': form, 'appointment': appointment})

def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if appointment.status != 'Canceled':
        appointment.status = 'Canceled'
        appointment.save()
    return redirect('appointments:appointment_list')

def complete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if appointment.status == 'Scheduled':
        appointment.status = 'Completed'
        appointment.save()
    return redirect('appointments:appointment_list')

def appointment_list(request):
    appointments = Appointment.objects.all().order_by('-appointment_time')
    return render(request, 'appointments/appointment_list.html', {'appointments': appointments})

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'appointments/employee_list.html', {'employees': employees})

def create_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('appointments:employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'appointments/create_employee.html', {'form': form})

def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('appointments:employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'appointments/edit_employee.html', {'form': form, 'employee': employee})

def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    return redirect('appointments:employee_list')

def service_list(request):
    services = Service.objects.all()
    return render(request, 'appointments/service_list.html', {'services': services})

def create_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointments:service_list')
    else:
        form = ServiceForm()
    return render(request, 'appointments/create_service.html', {'form': form})

def edit_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('appointments:service_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'appointments/edit_service.html', {'form': form, 'service': service})

def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    service.delete()
    return redirect('appointments:service_list')
