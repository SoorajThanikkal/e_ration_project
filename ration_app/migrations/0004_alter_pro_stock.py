# Generated by Django 5.0.2 on 2024-09-27 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ration_app', '0003_add2cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pro',
            name='stock',
            field=models.IntegerField(),
        ),
    ]
