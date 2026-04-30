from django.db import models
from django.contrib.auth.models import User


BRANCH_CHOICES = [
    ('CS', 'Computer Science & Engineering'),
    ('IT', 'Information Technology'),
    ('ECE', 'Electronics & Communication Engineering'),
    ('OTHER', 'Other'),
]

# Default subjects per branch used for seeding / UI hints
BRANCH_SUBJECTS = {
    'CS': [
        'Discrete Mathematics',
        'Data Structures & Algorithms',
        'Theory of Computation',
        'Compiler Design',
        'Computer Architecture & Organization',
        'Operating Systems',
        'Database Management Systems',
        'Artificial Intelligence',
        'Computer Networks',
        'Algorithm Design & Analysis',
        'Distributed Systems',
        'Computer Graphics',
        'Machine Learning',
        'Natural Language Processing',
        'Software Engineering',
    ],
    'IT': [
        'Programming for Problem Solving',
        'Data Structures',
        'Web Technologies',
        'Database Management Systems',
        'Computer Networks',
        'Operating Systems',
        'Software Engineering',
        'Cloud Computing',
        'IoT & Embedded Systems',
        'Machine Learning',
        'Cyber Security',
        'Mobile Application Development',
        'Big Data Analytics',
        'Human-Computer Interaction',
        'Information Security',
    ],
    'ECE': [
        'Circuit Theory',
        'Electronic Devices & Circuits',
        'Signals & Systems',
        'Digital Electronics',
        'Analog Communication',
        'Digital Communication',
        'VLSI Design',
        'Microprocessors & Interfacing',
        'Wireless Communication',
        'Embedded Systems',
        'RF & Microwave Engineering',
        'Digital Signal Processing',
        'Control Systems',
        'Optical Communication',
        'Antenna & Wave Propagation',
    ],
}


class Profile(models.Model):
    ROLE_CHOICES = [('teacher', 'Teacher'), ('student', 'Student')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    branch = models.CharField(max_length=10, choices=BRANCH_CHOICES, default='CS')

    def __str__(self):
        return f"{self.user.username} ({self.role} – {self.branch})"

    def is_teacher(self):
        return self.role == 'teacher'

    def is_student(self):
        return self.role == 'student'

    def get_branch_display_short(self):
        return self.branch


class Subject(models.Model):
    name = models.CharField(max_length=100)
    branch = models.CharField(max_length=10, choices=BRANCH_CHOICES, default='CS')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subjects')
    students = models.ManyToManyField(User, related_name='enrolled_subjects', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.branch}] {self.name}"


class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assignments')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_assignments')
    drive_link = models.URLField(blank=True, null=True, help_text="Public Google Drive link (optional)")
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    max_marks = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.title


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    drive_link = models.URLField(help_text="Public Google Drive link to your submission")
    submitted_at = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True)
    grade = models.CharField(max_length=10, blank=True, null=True)
    marks_obtained = models.PositiveIntegerField(blank=True, null=True)
    graded_at = models.DateTimeField(blank=True, null=True)
    graded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='graded_submissions')

    class Meta:
        unique_together = ('assignment', 'student')

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"


class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='notes')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    drive_link = models.URLField(blank=True, null=True, help_text="Public Google Drive link (optional)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
