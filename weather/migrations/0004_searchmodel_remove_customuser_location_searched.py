# Generated by Django 4.1 on 2023-08-20 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0003_alter_customuser_location_searched'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_searched', models.TextField(null=True)),
                ('username', models.CharField(max_length=50)),
                ('searched_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='location_searched',
        ),
    ]
