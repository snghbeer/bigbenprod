# Generated by Django 3.0.5 on 2020-08-01 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bigbenapp', '0002_auto_20200801_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]
