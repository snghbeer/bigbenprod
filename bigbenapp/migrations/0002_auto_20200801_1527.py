# Generated by Django 3.0.5 on 2020-08-01 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bigbenapp', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DateTimeTest',
        ),
        migrations.AlterField(
            model_name='appointment',
            name='time',
            field=models.TimeField(default='13'),
        ),
    ]
