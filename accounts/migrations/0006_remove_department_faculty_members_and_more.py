# Generated by Django 5.1.4 on 2025-01-11 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_department_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='faculty_members',
        ),
        migrations.RemoveField(
            model_name='department',
            name='programs',
        ),
    ]
