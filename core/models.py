from django.db import models
from django.contrib.auth.models import User


BRANCH_CHOICES = [
    # B.Tech
    ('BTECH_IT',   'B.Tech – Information Technology'),
    ('BTECH_CS',   'B.Tech – Computer Science & Engineering'),
    ('BTECH_ECE',  'B.Tech – Electronics & Communication Engineering'),
    # MCA
    ('MCA_IT',     'MCA – Information Technology'),
    # M.Tech
    ('MTECH_AIML', 'M.Tech – Artificial Intelligence & Machine Learning'),
    ('MTECH_DS',   'M.Tech – Data Science'),
]

DEPARTMENT_CHOICES = [
    ('BTECH', 'B.Tech'),
    ('MCA',   'MCA'),
    ('MTECH', 'M.Tech'),
]

BRANCH_SUBJECTS = {
    'BTECH_CS': [
        'Discrete Mathematics', 'Data Structures & Algorithms', 'Theory of Computation',
        'Compiler Design', 'Computer Architecture & Organization', 'Operating Systems',
        'Database Management Systems', 'Artificial Intelligence', 'Computer Networks',
        'Algorithm Design & Analysis', 'Machine Learning', 'Software Engineering',
    ],
    'BTECH_IT': [
        'Programming for Problem Solving', 'Data Structures', 'Web Technologies',
        'Database Management Systems', 'Computer Networks', 'Operating Systems',
        'Software Engineering', 'Cloud Computing', 'IoT & Embedded Systems',
        'Machine Learning', 'Cyber Security', 'Mobile Application Development',
    ],
    'BTECH_ECE': [
        'Circuit Theory', 'Electronic Devices & Circuits', 'Signals & Systems',
        'Digital Electronics', 'Analog Communication', 'Digital Communication',
        'VLSI Design', 'Microprocessors & Interfacing', 'Wireless Communication',
        'Embedded Systems', 'Digital Signal Processing', 'Control Systems',
    ],
    'MCA_IT': [
        'Programming in Python', 'Data Structures & Algorithms',
        'Database Management Systems', 'Computer Networks', 'Software Engineering',
        'Web Technologies', 'Cloud Computing', 'Cyber Security', 'Machine Learning',
    ],
    'MTECH_AIML': [
        'Advanced Machine Learning', 'Deep Learning', 'Natural Language Processing',
        'Computer Vision', 'Reinforcement Learning', 'AI Ethics & Governance',
        'Big Data Analytics', 'Research Methodology',
    ],
    'MTECH_DS': [
        'Statistical Methods', 'Data Mining', 'Big Data Technologies',
        'Machine Learning', 'Data Visualization', 'Database Systems',
        'Cloud Computing for Data Science', 'Research Methodology',
    ],
}


class Profile(models.Model):
    ROLE_CHOICES = [('teacher', 'Teacher'), ('student', 'Student')]
    user       = models.OneToOneField(User, on_delete=models.CASCADE)
    role       = models.CharField(max_length=10, choices=ROLE_CHOICES)
    branch     = models.CharField(max_length=20, choices=BRANCH_CHOICES, default='BTECH_CS')
    is_verified = models.BooleanField(default=False, help_text="Admin must verify before user can log in")

    def __str__(self):
        status = "✓" if self.is_verified else "⏳ Pending"
        return f"{self.user.username} ({self.role} – {self.branch}) {status}"

    def is_teacher(self):
        return self.role == 'teacher'

    def is_student(self):
        return self.role == 'student'

    def get_department(self):
        return self.branch.split('_')[0] if self.branch else ''


class Subject(models.Model):
    name       = models.CharField(max_length=100)
    branch     = models.CharField(max_length=20, choices=BRANCH_CHOICES, default='BTECH_CS')
    teacher    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subjects')
    students   = models.ManyToManyField(User, related_name='enrolled_subjects', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.branch}] {self.name}"


class Assignment(models.Model):
    title       = models.CharField(max_length=200)
    description = models.TextField()
    subject     = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assignments')
    teacher     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_assignments')
    drive_link  = models.URLField(blank=True, null=True)
    due_date    = models.DateTimeField()
    created_at  = models.DateTimeField(auto_now_add=True)
    max_marks   = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.title


class Submission(models.Model):
    assignment    = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    drive_link    = models.URLField()
    submitted_at  = models.DateTimeField(auto_now_add=True)
    remarks       = models.TextField(blank=True)
    grade         = models.CharField(max_length=10, blank=True, null=True)
    marks_obtained = models.PositiveIntegerField(blank=True, null=True)
    graded_at     = models.DateTimeField(blank=True, null=True)
    graded_by     = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='graded_submissions')

    class Meta:
        unique_together = ('assignment', 'student')

    def __str__(self):
        return f"{self.student.username} – {self.assignment.title}"


class Note(models.Model):
    title      = models.CharField(max_length=200)
    content    = models.TextField(blank=True)
    subject    = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='notes')
    teacher    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    drive_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
