# Generated by Django 5.0.7 on 2024-08-13 21:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_reply'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reply',
            old_name='comment',
            new_name='parent_comment',
        ),
    ]
