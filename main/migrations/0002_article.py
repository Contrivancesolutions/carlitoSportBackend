# Generated by Django 3.0.3 on 2020-02-15 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('preview', models.TextField()),
                ('content', models.TextField()),
                ('image', models.FileField(upload_to='')),
            ],
        ),
    ]