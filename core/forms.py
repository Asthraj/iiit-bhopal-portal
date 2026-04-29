from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Assignment, Submission, Note, Subject, BRANCH_CHOICES
from django.utils import timezone


class RegisterForm(UserCreationForm):
    ROLE_CHOICES = [('teacher', 'Teacher'), ('student', 'Student')]
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    branch = forms.ChoiceField(choices=BRANCH_CHOICES)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role', 'branch']


class AssignmentForm(forms.ModelForm):
    due_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Assignment
        fields = ['title', 'description', 'subject', 'file', 'due_date', 'max_marks']

    def __init__(self, teacher=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if teacher:
            self.fields['subject'].queryset = Subject.objects.filter(teacher=teacher)


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file', 'remarks']
        widgets = {'remarks': forms.Textarea(attrs={'rows': 3})}


class GradeForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['grade', 'marks_obtained', 'remarks']
        widgets = {'remarks': forms.Textarea(attrs={'rows': 3})}


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'subject', 'file']
        widgets = {'content': forms.Textarea(attrs={'rows': 5})}

    def __init__(self, teacher=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if teacher:
            self.fields['subject'].queryset = Subject.objects.filter(teacher=teacher)


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'branch', 'students']
        widgets = {'students': forms.CheckboxSelectMultiple()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        student_profiles = Profile.objects.filter(role='student')
        self.fields['students'].queryset = User.objects.filter(profile__in=student_profiles)
