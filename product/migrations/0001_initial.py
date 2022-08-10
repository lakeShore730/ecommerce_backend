# Generated by Django 4.0.6 on 2022-08-05 03:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=500)),
                ('image', models.ImageField(blank=True, null=True, upload_to='category_image')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.FloatField()),
                ('is_delivered', models.BooleanField(default=False)),
                ('is_deleted_by_user', models.BooleanField(default=False)),
                ('is_cancelled', models.BooleanField(default=False)),
                ('order_items', models.JSONField(default=[])),
                ('delivery_date', models.DateTimeField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.FloatField()),
                ('discount', models.FloatField(default=0)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('description', models.TextField(max_length=1000)),
                ('is_active', models.BooleanField(default=True)),
                ('primary_image', models.ImageField(upload_to='product_image')),
                ('secondary_image1', models.ImageField(blank=True, null=True, upload_to='product_image')),
                ('secondary_image2', models.ImageField(blank=True, null=True, upload_to='product_image')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('category', models.ManyToManyField(blank=True, null=True, to='product.category')),
            ],
        ),
    ]
