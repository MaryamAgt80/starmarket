# Generated by Django 4.1.3 on 2023-02-10 10:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0009_alter_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detilorder',
            name='product',
        ),
    ]
