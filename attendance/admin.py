from django.contrib import admin
from .models import Class, Module, Teacher, Student, ClassModule, Seance, AbsencePresence

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'class_obj')

@admin.register(ClassModule)
class ClassModuleAdmin(admin.ModelAdmin):
    list_display = ('class_obj', 'module', 'teacher')

@admin.register(Seance)
class SeanceAdmin(admin.ModelAdmin):
    list_display = ('date', 'classmodule')

@admin.register(AbsencePresence)
class AbsencePresenceAdmin(admin.ModelAdmin):
    list_display = ('student', 'session', 'status')
    list_filter = ('status', 'session__date')
