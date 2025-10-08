# Employee Management System

A comprehensive Django-based Employee Management System for managing employee records, departments, and organizational data.

## Features

- 📊 **Employee Dashboard** - Overview with statistics and metrics
- 👥 **Employee Management** - Complete CRUD operations for employees
- 🏢 **Department Management** - Organize employees by departments
- 🔍 **Advanced Search** - Search employees by name, department, role, etc.
- 📈 **Reports & Analytics** - Various reports and data analysis
- 📱 **Responsive Design** - Works on desktop and mobile devices
- ⚡ **AJAX Features** - Real-time validation and search

## Quick Start

### Prerequisites
- Python 3.8+
- Django 5.2+

### Installation

1. **Clone or download the project**
   ```bash
   cd employee_management
   ```

2. **Install dependencies**
   ```bash
   pip install django
   ```

3. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   - Main app: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

```
employee_management/
├── employee/                 # Main application
│   ├── models.py            # Database models
│   ├── views.py             # Business logic
│   ├── urls.py              # URL routing
│   ├── forms.py             # Form definitions
│   └── templates/           # HTML templates
│       └── employee/
│           ├── employee_form.html
│           ├── employee_list.html
│           ├── employee_detail.html
│           └── employee_confirm_delete.html
├── employee_management/     # Project settings
│   ├── settings.py          # Django settings
│   └── urls.py             # Project URL configuration
└── manage.py               # Django management script
```

## Key Features

### Employee Management
- Add new employees with comprehensive details
- Edit existing employee information
- View detailed employee profiles
- Delete employees with confirmation
- Bulk operations (export, import, delete)

### Department Management
- Create and manage departments
- Assign department managers
- Department-wise employee listing

### Search & Filters
- Real-time search across multiple fields
- Filter by department, status, gender
- Paginated results for large datasets

### Reports
- Employee summary reports
- Department-wise analytics
- Status and salary reports
- Data export to CSV

## Models

### Employee
- Personal information (name, email, phone, DOB, gender)
- Employment details (ID, department, role, salary, status)
- Location information (state, LGA, ward)
- Timestamps and status tracking

### Department
- Department name and description
- Department manager assignment
- Employee count tracking

## API Endpoints

- `GET /api/employees/` - List all employees
- `GET /api/employees/<id>/` - Get employee details
- `GET /api/departments/` - List all departments

## Utility Features

- Email uniqueness validation
- Employee ID auto-generation
- Phone number formatting
- Salary validation
- Data backup and restore options

## Customization

### Adding New Fields
Edit `employee/models.py` to add new fields to the Employee model.

### Modifying Forms
Update `employee/forms.py` to change form validation or field options.

### Styling
All CSS is included in the HTML templates. Modify the `<style>` sections in template files.

## Troubleshooting

### Common Issues

1. **"NoReverseMatch" error**
   - Check that all URL names in templates match those in `urls.py`

2. **Database errors**
   - Run `python manage.py makemigrations` and `python manage.py migrate`

3. **Static files not loading**
   - Ensure `DEBUG = True` in settings for development

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Verify all migrations are applied
3. Ensure all required fields are provided in forms

## License

This project is open source and available under the MIT License.

---

**Happy Managing!** 🚀
