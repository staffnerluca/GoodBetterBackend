# Generated by Django 5.0.7 on 2024-08-09 20:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_alter_userprofile_user_day'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Day',
            new_name='Days',
        ),
    ]