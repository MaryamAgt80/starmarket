# Generated by Django 4.1.3 on 2023-02-09 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0007_detilorder_detail_pooshak_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(0, 'پرداخت نشده'), (1, 'پرداخت شده'), (2, 'ارسال شده'), (3, 'دریافت شده')], default=0),
        ),
    ]
