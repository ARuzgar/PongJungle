# Generated by Django 4.2.10 on 2024-03-18 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api42', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, default='/code/media/images/', null=True, upload_to='images/', verbose_name='profile picture'),
        ),
    ]
