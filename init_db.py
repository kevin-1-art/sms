#!/usr/bin/env python
"""
Script to initialize the database with sample data.
Run after: python manage.py migrate
"""

import os
import django
from datetime import date, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.students.models import Student
from apps.teachers.models import Teacher
from apps.academics.models import Class, Subject, Result
from apps.attendance.models import Attendance

User = get_user_model()

def create_admin_user():
    """Create an admin user for testing."""
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@school.local',
            password='admin123',
            first_name='Admin',
            last_name='User',
            role='admin'
        )
        print("✓ Admin user created (username: admin, password: admin123)")

def create_classes():
    """Create sample classes."""
    classes_data = [
        {'name': 'Class 10-A', 'class_level': 10, 'section': 'A', 'capacity': 40},
        {'name': 'Class 10-B', 'class_level': 10, 'section': 'B', 'capacity': 40},
        {'name': 'Class 9-A', 'class_level': 9, 'section': 'A', 'capacity': 45},
        {'name': 'Class 9-B', 'class_level': 9, 'section': 'B', 'capacity': 45},
    ]
    
    for class_data in classes_data:
        Class.objects.get_or_create(
            class_level=class_data['class_level'],
            section=class_data['section'],
            defaults={
                'name': class_data['name'],
                'capacity': class_data['capacity']
            }
        )
    print(f"✓ Created {len(classes_data)} classes")

def create_subjects():
    """Create sample subjects."""
    subjects_data = [
        {'name': 'English', 'code': 'ENG101'},
        {'name': 'Mathematics', 'code': 'MAT101'},
        {'name': 'Science', 'code': 'SCI101'},
        {'name': 'History', 'code': 'HIS101'},
        {'name': 'Geography', 'code': 'GEO101'},
        {'name': 'Hindi', 'code': 'HIN101'},
    ]
    
    for subject_data in subjects_data:
        Subject.objects.get_or_create(
            code=subject_data['code'],
            defaults={'name': subject_data['name']}
        )
    print(f"✓ Created {len(subjects_data)} subjects")

def create_teachers():
    """Create sample teachers."""
    teachers_data = [
        {'username': 'teacher1', 'first_name': 'John', 'last_name': 'Smith', 
         'employee_id': 'EMP001', 'qualification': 'B.Ed', 'specialization': 'English'},
        {'username': 'teacher2', 'first_name': 'Sarah', 'last_name': 'Johnson',
         'employee_id': 'EMP002', 'qualification': 'M.Sc', 'specialization': 'Mathematics'},
        {'username': 'teacher3', 'first_name': 'Michael', 'last_name': 'Brown',
         'employee_id': 'EMP003', 'qualification': 'B.Sc', 'specialization': 'Science'},
    ]
    
    for teacher_data in teachers_data:
        if not User.objects.filter(username=teacher_data['username']).exists():
            user = User.objects.create_user(
                username=teacher_data['username'],
                email=f"{teacher_data['username']}@school.local",
                password='teacher123',
                first_name=teacher_data['first_name'],
                last_name=teacher_data['last_name'],
                role='teacher'
            )
            
            Teacher.objects.create(
                user=user,
                employee_id=teacher_data['employee_id'],
                qualification=teacher_data['qualification'],
                specialization=teacher_data['specialization'],
                date_of_joining=date.today()
            )
    
    print(f"✓ Created {len(teachers_data)} teachers")

def create_students():
    """Create sample students."""
    classes = Class.objects.all()
    if not classes.exists():
        print("⚠ No classes found. Create classes first.")
        return
    
    class_10_a = classes.first()
    
    students_data = [
        {'username': 'student1', 'first_name': 'Raj', 'last_name': 'Kumar',
         'admission_number': 'ADM001', 'gender': 'M', 'guardian_name': 'Ramesh Kumar'},
        {'username': 'student2', 'first_name': 'Priya', 'last_name': 'Singh',
         'admission_number': 'ADM002', 'gender': 'F', 'guardian_name': 'Rajesh Singh'},
        {'username': 'student3', 'first_name': 'Amit', 'last_name': 'Patel',
         'admission_number': 'ADM003', 'gender': 'M', 'guardian_name': 'Vikram Patel'},
    ]
    
    for student_data in students_data:
        if not User.objects.filter(username=student_data['username']).exists():
            user = User.objects.create_user(
                username=student_data['username'],
                email=f"{student_data['username']}@school.local",
                password='student123',
                first_name=student_data['first_name'],
                last_name=student_data['last_name'],
                role='student'
            )
            
            Student.objects.create(
                user=user,
                admission_number=student_data['admission_number'],
                gender=student_data['gender'],
                date_of_birth=date(2008, 1, 15),
                guardian_name=student_data['guardian_name'],
                guardian_phone='9876543210',
                guardian_address='123 Main Street, City',
                current_class=class_10_a
            )
    
    print(f"✓ Created {len(students_data)} students")

if __name__ == '__main__':
    print("\n🔧 Initializing School Management System Database...\n")
    
    create_admin_user()
    create_classes()
    create_subjects()
    create_teachers()
    create_students()
    
    print("\n✅ Database initialization complete!")
    print("\n📝 Sample Login Credentials:")
    print("   Admin:    username: admin, password: admin123")
    print("   Teacher:  username: teacher1, password: teacher123")
    print("   Student:  username: student1, password: student123")
    print("\n🚀 Run: python manage.py runserver\n")
