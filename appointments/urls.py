# urls.py

from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.index, name='index'),
    path('appointment-list/', views.appointment_list, name='appointment_list'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('cancel-appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('edit-appointment/<int:appointment_id>/', views.edit_appointment, name='edit_appointment'),
    path('complete-appointment/<int:appointment_id>/', views.complete_appointment, name='complete_appointment'),
    path('employee-list/', views.employee_list, name='employee_list'),
    path('create-employee/', views.create_employee, name='create_employee'),
    path('edit-employee/<int:employee_id>/', views.edit_employee, name='edit_employee'),
    path('delete-employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),
    path('service-list/', views.service_list, name='service_list'),
    path('create-service/', views.create_service, name='create_service'),
    path('edit-service/<int:pk>/', views.edit_service, name='edit_service'),
    path('delete-service/<int:pk>/', views.delete_service, name='delete_service'),
    path('inventory-list', views.inventory_list, name='inventory_list'),
    path('add/', views.inventory_add, name='inventory_add'),
    path('edit/<int:pk>/', views.inventory_edit, name='inventory_edit'),
    path('delete/<int:pk>/', views.inventory_delete, name='inventory_delete'),
    path('nail-design-list/', views.nail_design_list, name='nail_design_list'),
    path('create-nail-design/', views.create_nail_design, name='create_nail_design'),
    path('edit-nail-design/<int:pk>/', views.edit_nail_design, name='edit_nail_design'),
    path('delete-nail-design/<int:pk>/', views.delete_nail_design, name='delete_nail_design'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='user_logout'),
]

