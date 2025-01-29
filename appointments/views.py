from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Employee, Appointment, Inventory, NailDesign, Service
from .forms import AppointmentForm, EmployeeForm, InventoryForm, NailDesignForm, ServiceForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

# Check if the user is a staff member (admin)
def is_admin(user):
    return user.is_staff

# Customer Registration View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('appointments:index')  # Redirect to appointment list after registration
    else:
        form = UserCreationForm()
    return render(request, 'appointments/register.html', {'form': form})

# Login View
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('appointments:index')  # Redirect to appointment list after login
    else:
        form = AuthenticationForm()
    return render(request, 'appointments/login.html', {'form': form})

# Logout View
@login_required
def user_logout(request):
    logout(request)
    return redirect('appointments:login')  # Redirect to the login page after logging out

def index(request):
    return render(request, 'appointments/index.html')
    
@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment_time = form.cleaned_data['appointment_time']
            employee = form.cleaned_data['employee']
            services = form.cleaned_data['services']  # Get the selected services

            # Check if the appointment time is in the past
            if appointment_time < timezone.now():
                form.add_error('appointment_time', "You cannot book an appointment in the past.")
            else:
                # Check if the selected time slot is already booked
                existing_appointment = Appointment.objects.filter(
                    employee=employee,
                    appointment_time=appointment_time
                ).exclude(status='Canceled')
                if existing_appointment.exists():
                    form.add_error('appointment_time', "This time slot is already booked.")
                else:
                    appointment = form.save(commit=False)
                    appointment.user = request.user  # Associate the appointment with the logged-in user
                    appointment.save()
                    form.save_m2m()  # Save many-to-many relationships (services)
                    return redirect('appointments:appointment_list')
    else:
        form = AppointmentForm()

    return render(request, 'appointments/book_appointment.html', {'form': form})


@login_required
def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)  # Ensure the appointment belongs to the user
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointments:appointment_list')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'appointments/edit_appointment.html', {'form': form, 'appointment': appointment})

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)  # Ensure the appointment belongs to the user
    if appointment.status != 'Canceled':
        appointment.status = 'Canceled'
        appointment.save()
    return redirect('appointments:appointment_list')


@user_passes_test(is_admin)
def complete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if appointment.status == 'Scheduled':
        appointment.status = 'Completed'
        appointment.save()
    return redirect('appointments:appointment_list')


@login_required  # Ensures the user is logged in
def appointment_list(request):
    if request.user.is_staff:
        # Admins (staff users) can see all appointments
        appointments = Appointment.objects.all().order_by('-appointment_time')
    else:
        # Regular users can only see their own appointments
        appointments = Appointment.objects.filter(user=request.user).order_by('-appointment_time')

    return render(request, 'appointments/appointment_list.html', {'appointments': appointments})

@user_passes_test(is_admin)
def create_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('appointments:service_list')  # Redirect to service list
    else:
        form = ServiceForm()
    return render(request, 'appointments/service_form.html', {'form': form, 'action': 'Add'})


@user_passes_test(is_admin)
def edit_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            return redirect('appointments:service_list')  # Redirect to service list after editing
    else:
        form = ServiceForm(instance=service)
    return render(request, 'appointments/service_form.html', {'form': form, 'action': 'Edit'})


@user_passes_test(is_admin)
def delete_service(request, pk):
    if request.method == 'POST':
        service = get_object_or_404(Service, pk=pk)
        service.delete()
        return redirect('appointments:service_list')  # Redirect to service list after deletion
    return HttpResponse(status=405)  # Method Not Allowed for non-POST requests


def service_list(request):
    services = Service.objects.all()
    return render(request, 'appointments/service_list.html', {'services': services})

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'appointments/employee_list.html', {'employees': employees})

@user_passes_test(is_admin)
def create_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('appointments:employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'appointments/create_employee.html', {'form': form})

@user_passes_test(is_admin)
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

@user_passes_test(is_admin)
def delete_employee(request, employee_id):
    if request.method == 'POST':
        employee = get_object_or_404(Employee, id=employee_id)
        employee.delete()
        return redirect('appointments:employee_list')
    return HttpResponse(status=405)  # Method Not Allowed



    
def inventory_list(request):
    inventory_items = Inventory.objects.all()
    return render(request, 'appointments/inventory_list.html', {'inventory_items': inventory_items})

@user_passes_test(is_admin)
def inventory_add(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointments:inventory_list')
    else:
        form = InventoryForm()
    return render(request, 'appointments/inventory_form.html', {'form': form, 'action': 'Add'})

@user_passes_test(is_admin)
def inventory_edit(request, pk):
    inventory_item = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        form = InventoryForm(request.POST, instance=inventory_item)
        if form.is_valid():
            form.save()
            return redirect('appointments:inventory_list')
    else:
        form = InventoryForm(instance=inventory_item)
    return render(request, 'appointments/inventory_form.html', {'form': form, 'action': 'Edit'})

@user_passes_test(is_admin)
def inventory_delete(request, pk):
    if request.method == 'POST':
        inventory_item = get_object_or_404(Inventory, pk=pk)
        inventory_item.delete()
        return redirect('appointments:inventory_list')  # Redirect to inventory list after deletion
    return HttpResponse(status=405)  # Method Not Allowed for non-POST requests

@user_passes_test(is_admin)
def create_nail_design(request):
    if request.method == 'POST':
        form = NailDesignForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('appointments:nail_design_list')  # Redirect to list page after creation
    else:
        form = NailDesignForm()
    return render(request, 'appointments/nail_design_form.html', {'form': form, 'action': 'Add'})

@user_passes_test(is_admin)
def edit_nail_design(request, pk):
    nail_design = get_object_or_404(NailDesign, pk=pk)
    if request.method == 'POST':
        form = NailDesignForm(request.POST, request.FILES, instance=nail_design)
        if form.is_valid():
            form.save()
            return redirect('appointments:nail_design_list')  # Redirect to list page after editing
    else:
        form = NailDesignForm(instance=nail_design)
    return render(request, 'appointments/nail_design_form.html', {'form': form, 'action': 'Edit'})

@user_passes_test(is_admin)
def delete_nail_design(request, pk):
    if request.method == 'POST':
        nail_design = get_object_or_404(NailDesign, pk=pk)
        nail_design.delete()
        return redirect('appointments:nail_design_list')  # Redirect to nail design list after deletion
    return HttpResponse(status=405)  # Method Not Allowed for non-POST requests

def nail_design_list(request):
    nail_designs = NailDesign.objects.all()
    return render(request, 'appointments/nail_design_list.html', {'nail_designs': nail_designs})
