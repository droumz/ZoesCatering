# Generated by Django 4.2 on 2023-04-22 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
