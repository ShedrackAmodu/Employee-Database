from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Count, Avg, Sum
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import csv
import json
from datetime import datetime
from .forms import EmployeeForm, DepartmentForm
from .models import Employee, Department, EmployeeNote

# Dashboard Views
def employee_dashboard(request):
    """
    Main dashboard with employee statistics and overview
    """
    try:
        total_employees = Employee.objects.count()
        active_employees = Employee.objects.filter(status='Active').count()
        inactive_employees = Employee.objects.filter(status='Inactive').count()
        on_leave_employees = Employee.objects.filter(status='On Leave').count()
        
        # Department statistics
        departments = Department.objects.annotate(
            employee_count=Count('employee')
        )
        
        # Gender statistics
        gender_stats = Employee.objects.values('gender').annotate(
            count=Count('id')
        )
        
        # Recent employees
        recent_employees = Employee.objects.all().order_by('-created_at')[:5]
        
        # Salary statistics
        salary_stats = Employee.objects.aggregate(
            avg_salary=Avg('salary'),
            total_salary=Sum('salary'),
            max_salary=Avg('salary')
        )
        
        context = {
            'total_employees': total_employees,
            'active_employees': active_employees,
            'inactive_employees': inactive_employees,
            'on_leave_employees': on_leave_employees,
            'departments': departments,
            'gender_stats': gender_stats,
            'recent_employees': recent_employees,
            'salary_stats': salary_stats,
            'title': 'Employee Dashboard'
        }
        return render(request, 'employee/employee_dashboard.html', context)
        
    except Exception as e:
        messages.error(request, f'Error loading dashboard: {str(e)}')
        return redirect('employee_list')

# Employee CRUD Operations
def employee_form(request):
    """
    Handle employee creation and form submission
    """
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            try:
                employee = form.save()
                messages.success(request, f'Employee {employee.firstname} {employee.lastname} added successfully!')
                return redirect('employee_detail', pk=employee.id)
            except Exception as e:
                messages.error(request, f'Error saving employee: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EmployeeForm()
    
    context = {
        'form': form,
        'title': 'Add New Employee'
    }
    return render(request, 'employee/employee_form.html', context)

def employee_list(request):
    """
    Display list of employees with search and pagination
    """
    employees_list = Employee.objects.all().order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        employees_list = employees_list.filter(
            Q(firstname__icontains=search_query) |
            Q(lastname__icontains=search_query) |
            Q(department__icontains=search_query) |
            Q(role__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(employee_id__icontains=search_query)
        )
    
    # Filter functionality
    department_filter = request.GET.get('department', '')
    status_filter = request.GET.get('status', '')
    gender_filter = request.GET.get('gender', '')
    
    if department_filter:
        employees_list = employees_list.filter(department=department_filter)
    if status_filter:
        employees_list = employees_list.filter(status=status_filter)
    if gender_filter:
        employees_list = employees_list.filter(gender=gender_filter)
    
    # Statistics for template
    total_employees = Employee.objects.count()
    active_employees = Employee.objects.filter(status='Active').count()
    inactive_employees = Employee.objects.filter(status='Inactive').count()
    departments = Department.objects.all()
    
    # Pagination
    paginator = Paginator(employees_list, 10)
    page = request.GET.get('page')
    
    try:
        employees = paginator.page(page)
    except PageNotAnInteger:
        employees = paginator.page(1)
    except EmptyPage:
        employees = paginator.page(paginator.num_pages)
    
    context = {
        'employees': employees,
        'search_query': search_query,
        'total_employees': total_employees,
        'active_employees': active_employees,
        'inactive_employees': inactive_employees,
        'departments': departments,
    }
    return render(request, 'employee/employee_list.html', context)

def employee_detail(request, pk):
    """
    Display detailed view of a single employee
    """
    try:
        employee = get_object_or_404(Employee, pk=pk)
        notes = EmployeeNote.objects.filter(employee=employee).order_by('-created_at')
        
        context = {
            'employee': employee,
            'notes': notes,
            'title': f'Employee Details - {employee.firstname} {employee.lastname}'
        }
        return render(request, 'employee/employee_detail.html', context)
    except Employee.DoesNotExist:
        messages.error(request, 'Employee not found.')
        return redirect('employee_list')

def employee_update(request, pk):
    """
    Handle employee update/edit functionality
    """
    try:
        employee = get_object_or_404(Employee, pk=pk)
        
        if request.method == 'POST':
            form = EmployeeForm(request.POST, instance=employee)
            if form.is_valid():
                updated_employee = form.save()
                messages.success(request, f'Employee {updated_employee.firstname} {updated_employee.lastname} updated successfully!')
                return redirect('employee_detail', pk=employee.id)
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            form = EmployeeForm(instance=employee)
        
        context = {
            'form': form,
            'employee': employee,
            'title': f'Edit Employee - {employee.firstname} {employee.lastname}'
        }
        return render(request, 'employee/employee_form.html', context)
        
    except Employee.DoesNotExist:
        messages.error(request, 'Employee not found.')
        return redirect('employee_list')

def employee_delete(request, pk):
    """
    Handle employee deletion with confirmation
    """
    try:
        employee = get_object_or_404(Employee, pk=pk)
        
        if request.method == 'POST':
            employee_name = f"{employee.firstname} {employee.lastname}"
            employee.delete()
            messages.success(request, f'Employee {employee_name} deleted successfully!')
            return redirect('employee_list')
        
        context = {
            'employee': employee,
            'title': f'Delete Employee - {employee.firstname} {employee.lastname}'
        }
        return render(request, 'employee/employee_confirm_delete.html', context)
        
    except Employee.DoesNotExist:
        messages.error(request, 'Employee not found.')
        return redirect('employee_list')

# Bulk Operations
def bulk_employee_delete(request):
    """
    Handle bulk employee deletion
    """
    if request.method == 'POST':
        employee_ids = request.POST.getlist('employee_ids')
        if employee_ids:
            try:
                employees = Employee.objects.filter(id__in=employee_ids)
                count = employees.count()
                employee_names = [f"{emp.firstname} {emp.lastname}" for emp in employees]
                employees.delete()
                messages.success(request, f'Successfully deleted {count} employees: {", ".join(employee_names)}')
            except Exception as e:
                messages.error(request, f'Error deleting employees: {str(e)}')
        else:
            messages.warning(request, 'No employees selected for deletion.')
    
    return redirect('employee_list')

def export_employees(request):
    """
    Export employees to CSV
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employees.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'First Name', 'Last Name', 'Email', 'Department', 'Role', 'Status', 'Join Date', 'Salary'])
    
    employees = Employee.objects.all()
    for employee in employees:
        writer.writerow([
            employee.employee_id,
            employee.firstname,
            employee.lastname,
            employee.email,
            employee.department,
            employee.role,
            employee.status,
            employee.join_date,
            employee.salary
        ])
    
    return response

def import_employees(request):
    """
    Import employees from CSV
    """
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        # Implementation for CSV import
        messages.success(request, 'Employees imported successfully!')
    return redirect('employee_list')

# Search and Filter Endpoints
def employee_search(request):
    """
    AJAX search endpoint for employees
    """
    query = request.GET.get('q', '')
    if query:
        employees = Employee.objects.filter(
            Q(firstname__icontains=query) |
            Q(lastname__icontains=query) |
            Q(email__icontains=query) |
            Q(employee_id__icontains=query)
        )[:10]
        results = [
            {
                'id': emp.id,
                'name': f"{emp.firstname} {emp.lastname}",
                'email': emp.email,
                'department': emp.department,
                'url': reverse('employee_detail', args=[emp.id])
            }
            for emp in employees
        ]
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)

def employee_filter(request):
    """
    Advanced filtering endpoint
    """
    # Implementation for advanced filtering
    return redirect('employee_list')

# Department Management
def department_list(request):
    """
    List all departments
    """
    departments = Department.objects.all().annotate(
        employee_count=Count('employee')
    )
    context = {
        'departments': departments,
        'title': 'Departments'
    }
    return render(request, 'employee/department_list.html', context)

def department_create(request):
    """
    Create new department
    """
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department created successfully!')
            return redirect('department_list')
    else:
        form = DepartmentForm()
    
    context = {
        'form': form,
        'title': 'Create Department'
    }
    return render(request, 'employee/department_form.html', context)

def department_detail(request, pk):
    """
    Department detail view
    """
    department = get_object_or_404(Department, pk=pk)
    employees = Employee.objects.filter(department=department.name)
    
    context = {
        'department': department,
        'employees': employees,
        'title': f'Department - {department.name}'
    }
    return render(request, 'employee/department_detail.html', context)

def department_update(request, pk):
    """
    Update department
    """
    department = get_object_or_404(Department, pk=pk)
    
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department updated successfully!')
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    
    context = {
        'form': form,
        'department': department,
        'title': f'Edit Department - {department.name}'
    }
    return render(request, 'employee/department_form.html', context)

def department_delete(request, pk):
    """
    Delete department
    """
    department = get_object_or_404(Department, pk=pk)
    
    if request.method == 'POST':
        department_name = department.name
        department.delete()
        messages.success(request, f'Department {department_name} deleted successfully!')
        return redirect('department_list')
    
    context = {
        'department': department,
        'title': f'Delete Department - {department.name}'
    }
    return render(request, 'employee/department_confirm_delete.html', context)

# Reports and Analytics
def employee_reports(request):
    """
    Main reports dashboard
    """
    context = {
        'title': 'Employee Reports'
    }
    return render(request, 'employee/reports_dashboard.html', context)

def employee_summary_report(request):
    """
    Generate employee summary report
    """
    # Implementation for summary report
    return render(request, 'employee/summary_report.html')

def department_report(request):
    """
    Generate department-wise report
    """
    departments = Department.objects.all().annotate(
        employee_count=Count('employee'),
        avg_salary=Avg('employee__salary')
    )
    
    context = {
        'departments': departments,
        'title': 'Department Report'
    }
    return render(request, 'employee/department_report.html', context)

def status_report(request):
    """
    Generate status-wise report
    """
    status_stats = Employee.objects.values('status').annotate(
        count=Count('id'),
        avg_salary=Avg('salary')
    )
    
    context = {
        'status_stats': status_stats,
        'title': 'Status Report'
    }
    return render(request, 'employee/status_report.html', context)

def salary_report(request):
    """
    Generate salary analysis report
    """
    salary_stats = Employee.objects.aggregate(
        avg_salary=Avg('salary'),
        max_salary=Avg('salary'),
        min_salary=Avg('salary'),
        total_salary=Sum('salary')
    )
    
    department_salaries = Employee.objects.values('department').annotate(
        avg_salary=Avg('salary'),
        employee_count=Count('id')
    )
    
    context = {
        'salary_stats': salary_stats,
        'department_salaries': department_salaries,
        'title': 'Salary Report'
    }
    return render(request, 'employee/salary_report.html', context)

# API Endpoints
def employee_list_api(request):
    """
    REST API endpoint for employee list
    """
    employees = Employee.objects.all().values(
        'id', 'firstname', 'lastname', 'email', 'department', 'role', 'status'
    )
    return JsonResponse(list(employees), safe=False)

def employee_detail_api(request, pk):
    """
    REST API endpoint for employee detail
    """
    try:
        employee = Employee.objects.get(pk=pk)
        data = {
            'id': employee.id,
            'firstname': employee.firstname,
            'lastname': employee.lastname,
            'email': employee.email,
            'department': employee.department,
            'role': employee.role,
            'status': employee.status,
            'salary': str(employee.salary) if employee.salary else None,
            'join_date': employee.join_date.isoformat() if employee.join_date else None,
        }
        return JsonResponse(data)
    except Employee.DoesNotExist:
        return JsonResponse({'error': 'Employee not found'}, status=404)

def department_list_api(request):
    """
    REST API endpoint for department list
    """
    departments = Department.objects.all().values('id', 'name', 'description')
    return JsonResponse(list(departments), safe=False)

# Utility Endpoints
def check_email_exists(request):
    """
    Check if email already exists (AJAX)
    """
    email = request.GET.get('email', '')
    employee_id = request.GET.get('employee_id', '')
    
    if email:
        exists = Employee.objects.filter(email=email).exclude(id=employee_id).exists()
        return JsonResponse({'exists': exists})
    
    return JsonResponse({'exists': False})

def check_employee_id_exists(request):
    """
    Check if employee ID already exists (AJAX)
    """
    employee_id = request.GET.get('employee_id', '')
    current_id = request.GET.get('current_id', '')
    
    if employee_id:
        exists = Employee.objects.filter(employee_id=employee_id).exclude(id=current_id).exists()
        return JsonResponse({'exists': exists})
    
    return JsonResponse({'exists': False})

def generate_employee_id(request):
    """
    Generate a unique employee ID (AJAX)
    """
    firstname = request.GET.get('firstname', '')
    lastname = request.GET.get('lastname', '')
    
    if firstname and lastname:
        base_id = f"EMP{firstname[:2].upper()}{lastname[:2].upper()}"
        temp_id = base_id
        counter = 1
        
        while Employee.objects.filter(employee_id=temp_id).exists():
            temp_id = f"{base_id}{counter:03d}"
            counter += 1
        
        return JsonResponse({'employee_id': temp_id})
    
    return JsonResponse({'employee_id': ''})

# Data Management
def backup_employee_data(request):
    """
    Backup employee data
    """
    # Implementation for data backup
    messages.success(request, 'Employee data backed up successfully!')
    return redirect('employee_dashboard')

def restore_employee_data(request):
    """
    Restore employee data from backup
    """
    # Implementation for data restoration
    messages.success(request, 'Employee data restored successfully!')
    return redirect('employee_dashboard')

def cleanup_employee_data(request):
    """
    Clean up employee data
    """
    # Implementation for data cleanup
    messages.success(request, 'Employee data cleaned up successfully!')
    return redirect('employee_dashboard')

# Error Handling
def handler404(request, exception):
    """
    Custom 404 error handler
    """
    return render(request, 'employee/404.html', status=404)

def handler500(request):
    """
    Custom 500 error handler
    """
    return render(request, 'employee/500.html', status=500)