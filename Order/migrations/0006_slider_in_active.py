# Generated by Django 4.1.3 on 2023-02-09 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0005_slider'),
    ]

    operations = [
        migrations.AddField(
            model_name='slider',
            name='in_active',
            field=models.BooleanField(default=True),
        ),
    ]
