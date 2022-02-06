# Generated by Django 2.2.8 on 2021-08-04 17:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_subcategory_subcategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckIn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inStockOld', models.IntegerField()),
                ('inStockNew', models.IntegerField()),
                ('drink', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Drink')),
                ('history', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.History')),
            ],
        ),
    ]
