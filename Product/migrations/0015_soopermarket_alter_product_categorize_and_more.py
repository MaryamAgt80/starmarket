# Generated by Django 4.1.3 on 2023-02-07 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0014_remove_system_date_create_comment_date_comment_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='SooperMarket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(max_length=200)),
                ('use', models.TextField()),
                ('boad', models.CharField(max_length=20)),
                ('health_license', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='categorize',
            field=models.CharField(choices=[('Protein', 'Protein'), ('Dairy', 'Dairy'), ('Beans', 'Beans'), ('Digital', 'Digital'), ('Appliances', 'Appliances'), ('SooperMarket', 'SooperMarket')], default='Digital', max_length=20),
        ),
        migrations.AlterField(
            model_name='product',
            name='name_class',
            field=models.CharField(choices=[('Pooshak', 'Pooshak'), ('Phone', 'Phone'), ('System', 'System'), ('TV', 'TV'), ('Laundry', 'Laundry'), ('Refrigerator', 'Refrigerator'), ('Headset', 'Headset'), ('Case', 'Case'), ('keyboard', 'Keyboard'), ('SooperMarket', 'SooperMarket')], default='System', max_length=30, verbose_name='نام کلاس'),
        ),
    ]
