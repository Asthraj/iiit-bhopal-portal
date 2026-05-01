from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils import timezone
from .models import Profile, Assignment, Submission, Note, Subject, BRANCH_CHOICES
from .forms import RegisterForm, AssignmentForm, SubmissionForm, GradeForm, NoteForm, SubjectForm


# ---------- helpers ----------
DEPT_MAP = {
    'BTECH': 'B.Tech',
    'MCA':   'MCA',
    'MTECH': 'M.Tech',
}

def _get_profile(user):
    return get_object_or_404(Profile, user=user)


# ---------- public ----------

def home(request):
    """Public landing page — notes grouped by Subject (folder), only non-empty subjects shown."""
    branch_filter  = request.GET.get('branch', '')
    dept_filter    = request.GET.get('dept', '')

    subjects_qs = Subject.objects.order_by('branch', 'name')

    if dept_filter:
        subjects_qs = subjects_qs.filter(branch__startswith=dept_filter + '_')
    if branch_filter:
        subjects_qs = subjects_qs.filter(branch=branch_filter)

    # Only subjects that actually have notes
    subjects_with_notes = []
    for subj in subjects_qs:
        notes = subj.notes.all().order_by('-created_at')
        if notes.exists():
            subjects_with_notes.append({'subject': subj, 'notes': notes})

    return render(request, 'home.html', {
        'subjects_with_notes': subjects_with_notes,
        'branch_choices':      BRANCH_CHOICES,
        'branch_filter':       branch_filter,
        'dept_filter':         dept_filter,
        'dept_map':            DEPT_MAP,
    })


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True   # account exists but NOT verified yet
            user.save()
            Profile.objects.create(
                user=user,
                role=form.cleaned_data['role'],
                branch=form.cleaned_data['branch'],
                is_verified=False,   # admin must verify
            )
            messages.success(request,
                "✅ Account created! Please wait for admin approval before logging in.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # Check verification
            try:
                profile = user.profile
                if not profile.is_verified:
                    messages.error(request,
                        "⏳ Your account is pending admin approval. Please wait.")
                    return render(request, 'auth/login.html', {'form': form})
            except Profile.DoesNotExist:
                pass
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials. Please try again.")
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


# ---------- dashboard ----------

@login_required
def dashboard(request):
    profile = _get_profile(request.user)
    ctx = {'profile': profile}
    if profile.is_teacher():
        ctx['subjects']          = Subject.objects.filter(teacher=request.user)
        ctx['assignments']       = Assignment.objects.filter(teacher=request.user).order_by('-created_at')[:5]
        ctx['notes']             = Note.objects.filter(teacher=request.user).order_by('-created_at')[:5]
        ctx['total_submissions'] = Submission.objects.filter(assignment__teacher=request.user).count()
        ctx['pending_grading']   = Submission.objects.filter(assignment__teacher=request.user, grade__isnull=True).count()
    else:
        subjects            = request.user.enrolled_subjects.all()
        ctx['subjects']     = subjects
        assignments         = Assignment.objects.filter(subject__in=subjects).order_by('-created_at')
        ctx['assignments']  = assignments[:5]
        ctx['my_submissions'] = Submission.objects.filter(student=request.user).order_by('-submitted_at')[:5]
        ctx['pending_assignments'] = [
            a for a in assignments
            if not Submission.objects.filter(assignment=a, student=request.user).exists()
        ]
    return render(request, 'dashboard.html', ctx)


# ---------- subjects ----------

@login_required
def subject_list(request):
    profile = _get_profile(request.user)
    subjects = Subject.objects.filter(teacher=request.user) if profile.is_teacher() \
               else request.user.enrolled_subjects.all()
    return render(request, 'subjects/list.html', {'subjects': subjects, 'profile': profile})


@login_required
def subject_create(request):
    profile = _get_profile(request.user)
    if not profile.is_teacher():
        messages.error(request, "Only teachers can create subjects.")
        return redirect('subject_list')
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.teacher = request.user
            subject.save()
            form.save_m2m()
            messages.success(request, f'Subject "{subject.name}" created!')
            return redirect('subject_list')
    else:
        form = SubjectForm()
    return render(request, 'subjects/form.html', {'form': form, 'title': 'Create Subject'})


@login_required
def subject_detail(request, pk):
    subject     = get_object_or_404(Subject, pk=pk)
    profile     = _get_profile(request.user)
    assignments = subject.assignments.all().order_by('-created_at')
    notes       = subject.notes.all().order_by('-created_at')
    return render(request, 'subjects/detail.html', {
        'subject': subject, 'profile': profile,
        'assignments': assignments, 'notes': notes,
    })


# ---------- assignments ----------

@login_required
def assignment_list(request):
    profile = _get_profile(request.user)
    if profile.is_teacher():
        assignments = Assignment.objects.filter(teacher=request.user).order_by('-created_at')
    else:
        subjects    = request.user.enrolled_subjects.all()
        assignments = Assignment.objects.filter(subject__in=subjects).order_by('-created_at')
        for a in assignments:
            a.my_submission = Submission.objects.filter(assignment=a, student=request.user).first()
    return render(request, 'assignments/list.html', {'assignments': assignments, 'profile': profile})


@login_required
def assignment_create(request):
    profile = _get_profile(request.user)
    if not profile.is_teacher():
        messages.error(request, "Only teachers can create assignments.")
        return redirect('assignment_list')
    if request.method == 'POST':
        form = AssignmentForm(teacher=request.user, data=request.POST)
        if form.is_valid():
            assignment         = form.save(commit=False)
            assignment.teacher = request.user
            assignment.save()
            messages.success(request, f'Assignment "{assignment.title}" created!')
            return redirect('assignment_list')
    else:
        form = AssignmentForm(teacher=request.user)
    return render(request, 'assignments/form.html', {'form': form, 'title': 'Create Assignment'})


@login_required
def assignment_detail(request, pk):
    assignment    = get_object_or_404(Assignment, pk=pk)
    profile       = _get_profile(request.user)
    submissions   = None
    my_submission = None
    if profile.is_teacher():
        submissions = assignment.submissions.all().select_related('student')
    else:
        my_submission = Submission.objects.filter(assignment=assignment, student=request.user).first()
    return render(request, 'assignments/detail.html', {
        'assignment': assignment, 'profile': profile,
        'submissions': submissions, 'my_submission': my_submission,
    })


@login_required
def submit_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    profile    = _get_profile(request.user)
    if not profile.is_student():
        messages.error(request, "Only students can submit assignments.")
        return redirect('assignment_detail', pk=pk)
    existing = Submission.objects.filter(assignment=assignment, student=request.user).first()
    if existing:
        messages.warning(request, "You have already submitted this assignment.")
        return redirect('assignment_detail', pk=pk)
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            sub            = form.save(commit=False)
            sub.assignment = assignment
            sub.student    = request.user
            sub.save()
            messages.success(request, "Assignment submitted successfully!")
            return redirect('assignment_detail', pk=pk)
    else:
        form = SubmissionForm()
    return render(request, 'assignments/submit.html', {'form': form, 'assignment': assignment})


@login_required
def grade_submission(request, pk):
    submission = get_object_or_404(Submission, pk=pk)
    profile    = _get_profile(request.user)
    if not profile.is_teacher():
        messages.error(request, "Only teachers can grade submissions.")
        return redirect('dashboard')
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=submission)
        if form.is_valid():
            sub            = form.save(commit=False)
            sub.graded_by  = request.user
            sub.graded_at  = timezone.now()
            sub.save()
            messages.success(request, f"Graded {submission.student.get_full_name()}'s submission.")
            return redirect('assignment_detail', pk=submission.assignment.pk)
    else:
        form = GradeForm(instance=submission)
    return render(request, 'assignments/grade.html', {'form': form, 'submission': submission})


# ---------- notes ----------

@login_required
def note_list(request):
    profile = _get_profile(request.user)
    notes   = Note.objects.filter(teacher=request.user).order_by('-created_at') if profile.is_teacher() \
              else Note.objects.filter(subject__in=request.user.enrolled_subjects.all()).order_by('-created_at')
    return render(request, 'notes/list.html', {'notes': notes, 'profile': profile})


@login_required
def note_create(request):
    profile = _get_profile(request.user)
    if not profile.is_teacher():
        messages.error(request, "Only teachers can upload notes.")
        return redirect('note_list')
    if request.method == 'POST':
        form = NoteForm(teacher=request.user, data=request.POST)
        if form.is_valid():
            note         = form.save(commit=False)
            note.teacher = request.user
            note.save()
            messages.success(request, f'Note "{note.title}" uploaded!')
            return redirect('note_list')
    else:
        form = NoteForm(teacher=request.user)
    return render(request, 'notes/form.html', {'form': form, 'title': 'Upload Note'})


@login_required
def note_detail(request, pk):
    note    = get_object_or_404(Note, pk=pk)
    profile = _get_profile(request.user)
    return render(request, 'notes/detail.html', {'note': note, 'profile': profile})
