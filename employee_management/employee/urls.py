from django.urls import path, include
from django.views.generic import RedirectView
from . import views


urlpatterns = [
    # Dashboard and Homepage
    path('', views.employee_dashboard, name='employee_dashboard'),
    path('home/', views.employee_dashboard, name='employee_home'),
    
    # Employee CRUD Operations
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/create/', views.employee_form, name='employee_form'),
    path('employees/add/', views.employee_form, name='employee_add'),
    path('employees/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('employees/<int:pk>/edit/', views.employee_update, name='employee_update'),
    path('employees/<int:pk>/update/', views.employee_update, name='employee_update_alt'),
    path('employees/<int:pk>/delete/', views.employee_delete, name='employee_delete'),
    path('employees/<int:pk>/remove/', views.employee_delete, name='employee_remove'),
    
    # Bulk Operations
    path('employees/bulk-delete/', views.bulk_employee_delete, name='bulk_employee_delete'),
    path('employees/export/', views.export_employees, name='export_employees'),
    path('employees/import/', views.import_employees, name='import_employees'),
    
    # Search and Filter Endpoints
    path('employees/search/', views.employee_search, name='employee_search'),
    path('employees/filter/', views.employee_filter, name='employee_filter'),
    
    # Department Management
    path('departments/', views.department_list, name='department_list'),
    path('departments/create/', views.department_create, name='department_create'),
    path('departments/<int:pk>/', views.department_detail, name='department_detail'),
    path('departments/<int:pk>/edit/', views.department_update, name='department_update'),
    path('departments/<int:pk>/delete/', views.department_delete, name='department_delete'),
    
    # Reports and Analytics
    path('reports/', views.employee_reports, name='employee_reports'),
    path('reports/summary/', views.employee_summary_report, name='employee_summary_report'),
    path('reports/department/', views.department_report, name='department_report'),
    path('reports/status/', views.status_report, name='status_report'),
    path('reports/salary/', views.salary_report, name='salary_report'),
    
    # API Endpoints (RESTful)
    path('api/employees/', views.employee_list_api, name='employee_list_api'),
    path('api/employees/<int:pk>/', views.employee_detail_api, name='employee_detail_api'),
    path('api/departments/', views.department_list_api, name='department_list_api'),
    
    # Utility Endpoints
    path('employees/check-email/', views.check_email_exists, name='check_email_exists'),
    path('employees/check-employee-id/', views.check_employee_id_exists, name='check_employee_id_exists'),
    path('employees/generate-id/', views.generate_employee_id, name='generate_employee_id'),
    
    # Data Management
    path('employees/backup/', views.backup_employee_data, name='backup_employee_data'),
    path('employees/restore/', views.restore_employee_data, name='restore_employee_data'),
    path('employees/cleanup/', views.cleanup_employee_data, name='cleanup_employee_data'),
    
    # Redirects for backward compatibility
    path('form/', RedirectView.as_view(pattern_name='employees:employee_form', permanent=True)),
    path('list/', RedirectView.as_view(pattern_name='employees:employee_list', permanent=True)),
    path('detail/<int:pk>/', RedirectView.as_view(pattern_name='employees:employee_detail', permanent=True)),
    path('update/<int:pk>/', RedirectView.as_view(pattern_name='employees:employee_update', permanent=True)),
    path('delete/<int:pk>/', RedirectView.as_view(pattern_name='employees:employee_delete', permanent=True)),
]

# Optional: Include Django REST Framework URLs if using DRF
# urlpatterns += [
#     path('api/', include('rest_framework.urls')),
# ]

# Optional: Include Django admin URLs
# from django.contrib import admin
# urlpatterns += [
#     path('admin/', admin.site.urls),
# ]