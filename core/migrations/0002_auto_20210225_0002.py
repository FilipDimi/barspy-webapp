# Generated by Django 2.2.8 on 2021-02-25 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='date',
            field=models.CharField(max_length=20),
        ),
    ]
