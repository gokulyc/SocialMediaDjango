# Generated by Django 3.0.6 on 2020-06-17 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Connect', '0006_auto_20200616_1800'),
    ]

    operations = [
        migrations.AddField(
            model_name='company_model',
            name='map_embed',
            field=models.TextField(blank=True, null=True),
        ),
    ]