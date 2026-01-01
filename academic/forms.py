from django import forms
from attendance.models import Seance, ClassModule, Teacher

class SessionForm(forms.ModelForm):
    class Meta:
        model = Seance
        fields = ['classmodule', 'date', 'start_time', 'end_time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'classmodule': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            try:
                teacher_obj = Teacher.objects.get(user=user)
                self.fields['classmodule'].queryset = ClassModule.objects.filter(teacher=teacher_obj)
            except Teacher.DoesNotExist:
                self.fields['classmodule'].queryset = ClassModule.objects.none()
