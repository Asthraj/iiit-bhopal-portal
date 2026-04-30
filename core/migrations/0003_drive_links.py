from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_add_branch'),
    ]

    operations = [
        # Assignment: remove file, add drive_link
        migrations.RemoveField(
            model_name='assignment',
            name='file',
        ),
        migrations.AddField(
            model_name='assignment',
            name='drive_link',
            field=models.URLField(blank=True, null=True, help_text='Public Google Drive link (optional)'),
        ),
        # Submission: remove file, add drive_link
        migrations.RemoveField(
            model_name='submission',
            name='file',
        ),
        migrations.AddField(
            model_name='submission',
            name='drive_link',
            field=models.URLField(default='', help_text='Public Google Drive link to your submission'),
            preserve_default=False,
        ),
        # Note: remove file, add drive_link
        migrations.RemoveField(
            model_name='note',
            name='file',
        ),
        migrations.AddField(
            model_name='note',
            name='drive_link',
            field=models.URLField(blank=True, null=True, help_text='Public Google Drive link (optional)'),
        ),
    ]
