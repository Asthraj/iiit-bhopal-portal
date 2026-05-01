from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='branch',
            field=models.CharField(
                choices=[
                    ('CS', 'Computer Science & Engineering'),
                    ('IT', 'Information Technology'),
                    ('ECE', 'Electronics & Communication Engineering'),
                    ('OTHER', 'Other'),
                ],
                default='CS',
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name='subject',
            name='branch',
            field=models.CharField(
                choices=[
                    ('CS', 'Computer Science & Engineering'),
                    ('IT', 'Information Technology'),
                    ('ECE', 'Electronics & Communication Engineering'),
                    ('OTHER', 'Other'),
                ],
                default='CS',
                max_length=10,
            ),
        ),
    ]
