from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from attendance.models import AbsencePresence, Seance, Module, Student, Teacher
# Aliases
AttendanceRecord = AbsencePresence
Session = Seance
from django.db.models import Count

@login_required
def dashboard(request):
    user = request.user
    if user.role == 'student':
        return redirect('student_dashboard')
    elif user.role == 'teacher':
        return redirect('teacher_dashboard')
    elif user.role == 'admin':
        return redirect('admin:index')
    return render(request, 'base.html')

@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        return redirect('dashboard')
        
    try:
        student_obj = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return render(request, 'dashboard_student.html', {'chart_labels': [], 'chart_data': [], 'recent_records': []})

    # Get modules the student has attended at least once
    records = AttendanceRecord.objects.filter(student=student_obj)
    module_ids = records.values_list('session__classmodule__module', flat=True).distinct()
    
    modules_data = [] # Names
    attendance_data = [] # Percentages
    
    for mid in module_ids:
        module = Module.objects.get(pk=mid)
        total_sessions = Session.objects.filter(classmodule__module=module, classmodule__class_obj=student_obj.class_obj).count()
        my_attendance = records.filter(session__classmodule__module=module).count()
        
        if total_sessions > 0:
            percentage = (my_attendance / total_sessions) * 100
        else:
            percentage = 0
            
        modules_data.append(module.name)
        attendance_data.append(round(percentage, 1))

    context = {
        'chart_labels': modules_data,
        'chart_data': attendance_data,
        'recent_records': records.order_by('-timestamp')[:5]
    }
    return render(request, 'dashboard_student.html', context)

@login_required
def teacher_dashboard(request):
    if request.user.role != 'teacher':
        return redirect('dashboard')
        
    teacher_obj, created = Teacher.objects.get_or_create(user=request.user)

    from attendance.models import ClassModule
    class_modules = ClassModule.objects.filter(teacher=teacher_obj).select_related('class_obj', 'module')
    
    labels = []
    total_attendances = []
    
    for cm in class_modules:
        # Total check-ins for this class+module across all sessions
        count = AttendanceRecord.objects.filter(session__classmodule=cm).count()
        labels.append(f"{cm.class_obj.name} - {cm.module.name}")
        total_attendances.append(count)
        
    context = {
        'courses': class_modules,
        'chart_labels': labels,
        'chart_data': total_attendances,
        'total_checkins': sum(total_attendances)
    }
    return render(request, 'dashboard_teacher.html', context)

from .forms import ProfileUpdateForm
from django.contrib import messages

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})
