# Generated by Django 4.2.5 on 2023-09-28 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iptv', '0002_alter_video_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='icon',
            field=models.FileField(upload_to='icons/'),
        ),
    ]
