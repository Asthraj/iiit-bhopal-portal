from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_drive_links'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_verified',
            field=models.BooleanField(default=False, help_text='Admin must verify before user can log in'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='branch',
            field=models.CharField(
                choices=[
                    ('BTECH_IT',   'B.Tech – Information Technology'),
                    ('BTECH_CS',   'B.Tech – Computer Science & Engineering'),
                    ('BTECH_ECE',  'B.Tech – Electronics & Communication Engineering'),
                    ('MCA_IT',     'MCA – Information Technology'),
                    ('MTECH_AIML', 'M.Tech – Artificial Intelligence & Machine Learning'),
                    ('MTECH_DS',   'M.Tech – Data Science'),
                ],
                default='BTECH_CS',
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name='subject',
            name='branch',
            field=models.CharField(
                choices=[
                    ('BTECH_IT',   'B.Tech – Information Technology'),
                    ('BTECH_CS',   'B.Tech – Computer Science & Engineering'),
                    ('BTECH_ECE',  'B.Tech – Electronics & Communication Engineering'),
                    ('MCA_IT',     'MCA – Information Technology'),
                    ('MTECH_AIML', 'M.Tech – Artificial Intelligence & Machine Learning'),
                    ('MTECH_DS',   'M.Tech – Data Science'),
                ],
                default='BTECH_CS',
                max_length=20,
            ),
        ),
    ]
