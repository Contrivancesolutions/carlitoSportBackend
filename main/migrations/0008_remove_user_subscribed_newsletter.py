# Generated by Django 3.0.3 on 2020-03-05 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20200305_1511'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='subscribed_newsletter',
        ),
    ]