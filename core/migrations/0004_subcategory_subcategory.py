# Generated by Django 3.0.4 on 2021-03-11 03:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210308_2356'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='subcategory',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.Category'),
            preserve_default=False,
        ),
    ]
