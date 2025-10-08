from django import forms
from .models import Employee, Department

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'firstname', 'lastname', 'othername', 'email', 'department', 
            'dob', 'gender', 'state', 'lga', 'ward', 'role',
            'employee_id', 'phone', 'join_date', 'salary', 'status'
        ]
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'join_date': forms.DateInput(attrs={'type': 'date'}),
            'firstname': forms.TextInput(attrs={'placeholder': 'Enter first name'}),
            'lastname': forms.TextInput(attrs={'placeholder': 'Enter last name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email address'}),
            'department': forms.TextInput(attrs={'placeholder': 'Enter department'}),
            'role': forms.TextInput(attrs={'placeholder': 'Enter role'}),
            'state': forms.TextInput(attrs={'placeholder': 'Enter state'}),
            'lga': forms.TextInput(attrs={'placeholder': 'Enter LGA'}),
            'ward': forms.TextInput(attrs={'placeholder': 'Enter ward'}),
            'employee_id': forms.TextInput(attrs={'placeholder': 'Optional employee ID'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Optional phone number'}),
            'salary': forms.NumberInput(attrs={'placeholder': 'Optional salary', 'step': '0.01'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        
        # Add CSS classes to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input'
            
        # Set required fields
        self.fields['firstname'].required = True
        self.fields['lastname'].required = True
        self.fields['email'].required = True
        self.fields['department'].required = True
        self.fields['dob'].required = True
        self.fields['gender'].required = True
        self.fields['state'].required = True
        self.fields['lga'].required = True
        self.fields['ward'].required = True
        self.fields['role'].required = True
        
        # Optional fields
        self.fields['othername'].required = False
        self.fields['employee_id'].required = False
        self.fields['phone'].required = False
        self.fields['join_date'].required = False
        self.fields['salary'].required = False
        
        # Add asterisk to required field labels
        self.fields['firstname'].label = 'First Name *'
        self.fields['lastname'].label = 'Last Name *'
        self.fields['email'].label = 'Email *'
        self.fields['department'].label = 'Department *'
        self.fields['dob'].label = 'Date of Birth *'
        self.fields['gender'].label = 'Gender *'
        self.fields['state'].label = 'State *'
        self.fields['lga'].label = 'LGA *'
        self.fields['ward'].label = 'Ward *'
        self.fields['role'].label = 'Role *'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Check if email already exists (for new records)
        if not self.instance.pk:  # This is a new record
            if Employee.objects.filter(email=email).exists():
                raise forms.ValidationError("An employee with this email already exists.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Basic phone validation - you can customize this
            if not phone.replace(' ', '').replace('-', '').replace('+', '').isdigit():
                raise forms.ValidationError("Please enter a valid phone number.")
        return phone

    def clean_salary(self):
        salary = self.cleaned_data.get('salary')
        if salary and salary < 0:
            raise forms.ValidationError("Salary cannot be negative.")
        return salary


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description', 'manager']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter department name',
                'class': 'form-input'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Enter department description (optional)',
                'class': 'form-input',
                'rows': 4
            }),
            'manager': forms.Select(attrs={
                'class': 'form-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)
        
        # Add CSS classes to all fields
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-input'
        
        # Set required fields
        self.fields['name'].required = True
        self.fields['name'].label = 'Department Name *'
        
        # Optional fields
        self.fields['description'].required = False
        self.fields['manager'].required = False
        
        # Limit manager choices to active employees only
        self.fields['manager'].queryset = Employee.objects.filter(status='Active')

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            name = name.strip().title()
            # Check if department name already exists (for new records)
            if not self.instance.pk:  # This is a new record
                if Department.objects.filter(name=name).exists():
                    raise forms.ValidationError("A department with this name already exists.")
        return name