# Generated by Django 4.2 on 2023-04-22 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_rename_options_option'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='product_imgs/')),
                ('slug', models.CharField(max_length=400)),
                ('detail', models.TextField()),
                ('status', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.category')),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.option')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.size')),
            ],
        ),
    ]
