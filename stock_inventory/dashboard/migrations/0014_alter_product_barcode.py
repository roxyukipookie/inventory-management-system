# Generated by Django 5.1.2 on 2024-11-28 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0013_alter_product_barcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='barcode',
            field=models.IntegerField(unique=True),
        ),
    ]
