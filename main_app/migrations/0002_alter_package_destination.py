# Generated by Django 5.0.6 on 2024-06-05 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='destination',
            field=models.CharField(choices=[('Mo', 'Moon'), ('Ma', 'Mars'), ('Pl', 'Pluto'), ('Is', 'Internation Space Station'), ('Ne', 'Neptune')], default=0, max_length=2),
        ),
    ]
