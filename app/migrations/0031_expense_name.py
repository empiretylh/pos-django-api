# Generated by Django 3.2.9 on 2023-10-15 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0030_soldproduct_productid'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='name',
            field=models.CharField(default='', max_length=255, null=True),
        ),
    ]
