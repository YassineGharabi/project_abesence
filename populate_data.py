import os
import django
from django.utils import timezone
import datetime
import uuid

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_project.settings')
django.setup()

from accounts.models import User
from attendance.models import Class, Module, Teacher, Student, ClassModule, Seance, AbsencePresence

def populate():
    print("Populating data...")

    # 1. Create Classes
    class_a, _ = Class.objects.get_or_create(name="Class A")
    class_b, _ = Class.objects.get_or_create(name="Class B")

    # 2. Create Modules
    math, _ = Module.objects.get_or_create(name="Mathematics")
    physics, _ = Module.objects.get_or_create(name="Physics")

    # 3. Create Users and Teacher/Student profiles
    
    # Teachers
    t1_user, created = User.objects.get_or_create(username="teacher1", role="teacher")
    if created: t1_user.set_password("password123"); t1_user.save()
    teacher1, _ = Teacher.objects.get_or_create(user=t1_user)

    t2_user, created = User.objects.get_or_create(username="teacher2", role="teacher")
    if created: t2_user.set_password("password123"); t2_user.save()
    teacher2, _ = Teacher.objects.get_or_create(user=t2_user)

    # Students
    s1_user, created = User.objects.get_or_create(username="student1", role="student")
    if created: s1_user.set_password("password123"); s1_user.save()
    student1, _ = Student.objects.get_or_create(user=s1_user, class_obj=class_a)

    s2_user, created = User.objects.get_or_create(username="student2", role="student")
    if created: s2_user.set_password("password123"); s2_user.save()
    student2, _ = Student.objects.get_or_create(user=s2_user, class_obj=class_a)

    s3_user, created = User.objects.get_or_create(username="student3", role="student")
    if created: s3_user.set_password("password123"); s3_user.save()
    student3, _ = Student.objects.get_or_create(user=s3_user, class_obj=class_b)

    # 4. Create ClassModules
    cm1, _ = ClassModule.objects.get_or_create(class_obj=class_a, module=math, teacher=teacher1)
    cm2, _ = ClassModule.objects.get_or_create(class_obj=class_b, module=physics, teacher=teacher2)

    # 5. Create Seances
    seance1, _ = Seance.objects.get_or_create(
        date=datetime.date.today(), 
        classmodule=cm1,
        defaults={
            'start_time': datetime.time(8, 0),
            'end_time': datetime.time(10, 0),
            'token': str(uuid.uuid4())
        }
    )
    seance2, _ = Seance.objects.get_or_create(
        date=datetime.date.today(), 
        classmodule=cm2,
        defaults={
            'start_time': datetime.time(10, 0),
            'end_time': datetime.time(12, 0),
            'token': str(uuid.uuid4())
        }
    )

    # 6. Create AbsencePresence
    AbsencePresence.objects.get_or_create(student=student1, session=seance1, status='present')
    AbsencePresence.objects.get_or_create(student=student2, session=seance1, status='absent')
    AbsencePresence.objects.get_or_create(student=student3, session=seance2, status='present')

    print("Data population complete!")

if __name__ == "__main__":
    populate()
