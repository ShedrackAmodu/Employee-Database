from django.db import models
from django.core.validators import MinLengthValidator, EmailValidator
from django.utils import timezone
from django.urls import reverse
import uuid

class Employee(models.Model):
    # Primary Key
    id = models.AutoField(primary_key=True)
    
    # Personal Information
    firstname = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)],
        help_text="Enter employee's first name",
        verbose_name="First Name"
    )
    lastname = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)],
        help_text="Enter employee's last name",
        verbose_name="Last Name"
    )
    othername = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Enter employee's other name (optional)",
        verbose_name="Other Name"
    )
    
    # Contact Information
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator()],
        help_text="Enter valid email address",
        verbose_name="Email Address"
    )
    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text="Enter phone number (optional)",
        verbose_name="Phone Number"
    )
    
    # Employment Information
    employee_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True,
        help_text="Unique employee ID (optional)",
        verbose_name="Employee ID"
    )
    department = models.CharField(
        max_length=100,
        help_text="Enter department name",
        verbose_name="Department"
    )
    role = models.CharField(
        max_length=100,
        help_text="Enter job role",
        verbose_name="Job Role"
    )
    join_date = models.DateField(
        blank=True,
        null=True,
        help_text="Select join date",
        verbose_name="Join Date"
    )
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Enter salary amount",
        verbose_name="Salary"
    )
    
    # Personal Details
    dob = models.DateField(
        help_text="Select date of birth",
        verbose_name="Date of Birth"
    )
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        help_text="Select gender",
        verbose_name="Gender"
    )
    
    # Location Information
    state = models.CharField(
        max_length=50,
        help_text="Enter state",
        verbose_name="State"
    )
    lga = models.CharField(
        max_length=50,
        help_text="Enter Local Government Area",
        verbose_name="LGA"
    )
    ward = models.CharField(
        max_length=100,
        help_text="Enter ward",
        verbose_name="Ward"
    )
    
    # Status Information
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Suspended', 'Suspended'),
        ('On Leave', 'On Leave'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Active',
        help_text="Select employee status",
        verbose_name="Employment Status"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Metadata
    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['lastname', 'firstname']),
            models.Index(fields=['department']),
            models.Index(fields=['status']),
            models.Index(fields=['email']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['email'],
                name='unique_employee_email'
            ),
            models.UniqueConstraint(
                fields=['employee_id'],
                condition=models.Q(employee_id__isnull=False),
                name='unique_employee_id_when_not_null'
            ),
        ]
    
    def __str__(self):
        return f'{self.firstname} {self.lastname}'
    
    def get_absolute_url(self):
        return reverse('employee_detail', kwargs={'pk': self.pk})
    
    def get_full_name(self):
        """Return the full name of the employee"""
        if self.othername:
            return f'{self.firstname} {self.othername} {self.lastname}'
        return f'{self.firstname} {self.lastname}'
    
    def get_age(self):
        """Calculate employee's age"""
        if self.dob:
            today = timezone.now().date()
            return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return None
    
    def get_years_of_service(self):
        """Calculate years of service"""
        if self.join_date:
            today = timezone.now().date()
            return today.year - self.join_date.year - ((today.month, today.day) < (self.join_date.month, self.join_date.day))
        return None
    
    def is_active(self):
        """Check if employee is active"""
        return self.status == 'Active'
    
    def save(self, *args, **kwargs):
        # Generate employee ID if not provided
        if not self.employee_id:
            self.employee_id = self.generate_employee_id()
        
        # Ensure email is lowercase
        if self.email:
            self.email = self.email.lower()
        
        super().save(*args, **kwargs)
    
    def generate_employee_id(self):
        """Generate a unique employee ID"""
        base_id = f"EMP{self.firstname[:2].upper()}{self.lastname[:2].upper()}"
        temp_id = base_id
        counter = 1
        
        # Check if this ID already exists and find a unique one
        while Employee.objects.filter(employee_id=temp_id).exists():
            temp_id = f"{base_id}{counter:03d}"
            counter += 1
        
        return temp_id
    
    @property
    def formatted_salary(self):
        """Return formatted salary with currency"""
        if self.salary:
            return f"${self.salary:,.2f}"
        return "Not set"
    
    @property
    def formatted_join_date(self):
        """Return formatted join date"""
        if self.join_date:
            return self.join_date.strftime("%b %d, %Y")
        return "Not set"
    
    @property
    def formatted_dob(self):
        """Return formatted date of birth"""
        if self.dob:
            return self.dob.strftime("%b %d, %Y")
        return "Not set"

class Department(models.Model):
    """Model to manage departments"""
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Enter department name",
        verbose_name="Department Name"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Enter department description",
        verbose_name="Description"
    )
    manager = models.ForeignKey(
        'Employee',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='managed_departments',
        help_text="Select department manager",
        verbose_name="Department Manager"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_employee_count(self):
        """Return number of employees in this department"""
        return Employee.objects.filter(department=self.name).count()

class EmployeeNote(models.Model):
    """Model to store notes about employees"""
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='notes',
        help_text="Select employee",
        verbose_name="Employee"
    )
    note = models.TextField(
        help_text="Enter note about employee",
        verbose_name="Note"
    )
    created_by = models.CharField(
        max_length=100,
        help_text="Enter your name",
        verbose_name="Created By"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Employee Note"
        verbose_name_plural = "Employee Notes"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Note for {self.employee} - {self.created_at.strftime('%Y-%m-%d')}"

# Signal imports (add these at the bottom if you want to use signals)
from django.db.models.signals import pre_save
from django.dispatch import receiver

@receiver(pre_save, sender=Employee)
def employee_pre_save(sender, instance, **kwargs):
    """
    Signal to perform actions before saving an employee
    """
    # Ensure firstname and lastname are properly capitalized
    if instance.firstname:
        instance.firstname = instance.firstname.strip().title()
    if instance.lastname:
        instance.lastname = instance.lastname.strip().title()
    if instance.othername:
        instance.othername = instance.othername.strip().title()
    
    # Capitalize department, role, state, lga, ward
    if instance.department:
        instance.department = instance.department.strip().title()
    if instance.role:
        instance.role = instance.role.strip().title()
    if instance.state:
        instance.state = instance.state.strip().title()
    if instance.lga:
        instance.lga = instance.lga.strip().title()
    if instance.ward:
        instance.ward = instance.ward.strip().title()