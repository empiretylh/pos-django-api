# Generated by Django 3.2.9 on 2022-08-28 05:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_soldproduct_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='soldproduct',
            name='sales',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sproduct', to='app.sales'),
        ),
    ]
