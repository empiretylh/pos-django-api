# Generated by Django 3.2.9 on 2022-08-27 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20220807_1745'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
