# Generated by Django 3.0.6 on 2020-06-14 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Connect', '0002_auto_20200614_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdatabase',
            name='profile_title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
