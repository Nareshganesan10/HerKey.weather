# Generated by Django 4.1 on 2023-08-20 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0002_rename_user_address_customuser_user_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='location_searched',
            field=models.TextField(null=True),
        ),
    ]
