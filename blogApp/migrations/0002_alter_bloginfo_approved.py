# Generated by Django 3.2.25 on 2024-10-09 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloginfo',
            name='approved',
            field=models.BooleanField(null=True),
        ),
    ]
