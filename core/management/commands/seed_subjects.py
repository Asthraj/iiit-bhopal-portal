"""
Management command to seed default branch-wise subjects for IIIT Bhopal.

Usage:
    python manage.py seed_subjects --teacher <username>

The teacher account must exist before running this command.
"""
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from core.models import Subject, BRANCH_SUBJECTS


class Command(BaseCommand):
    help = 'Seeds default IT / CS / ECE subjects for IIIT Bhopal portal'

    def add_arguments(self, parser):
        parser.add_argument(
            '--teacher',
            type=str,
            required=True,
            help='Username of the teacher who will own the seeded subjects',
        )

    def handle(self, *args, **options):
        username = options['teacher']
        try:
            teacher = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f'Teacher "{username}" does not exist.')

        created_count = 0
        for branch, subjects in BRANCH_SUBJECTS.items():
            for name in subjects:
                _, created = Subject.objects.get_or_create(
                    name=name,
                    branch=branch,
                    teacher=teacher,
                )
                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f'  [{branch}] {name}'))

        self.stdout.write(
            self.style.SUCCESS(f'\n✅  Done! {created_count} subjects seeded under teacher "{username}".')
        )
