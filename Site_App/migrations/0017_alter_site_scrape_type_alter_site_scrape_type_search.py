# Generated by Django 4.2.5 on 2023-10-04 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Site_App', '0016_alter_site_scrape_type_search'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site_scrape',
            name='type',
            field=models.IntegerField(verbose_name='روش جستوجو'),
        ),
        migrations.AlterField(
            model_name='site_scrape',
            name='type_search',
            field=models.IntegerField(default=0, verbose_name='نوع خراش'),
        ),
    ]
