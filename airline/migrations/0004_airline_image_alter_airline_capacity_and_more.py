# Generated by Django 5.0.7 on 2024-07-21 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airline', '0003_remove_airline_phone_airline_takeoff_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='airline',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='airline',
            name='capacity',
            field=models.CharField(blank=True, max_length=240, null=True),
        ),
        migrations.AlterField(
            model_name='airline',
            name='destination_city',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='airline',
            name='origin_city',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='airline',
            name='seats_used',
            field=models.CharField(blank=True, max_length=240, null=True),
        ),
        migrations.AlterField(
            model_name='airline',
            name='takeoff_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='orderflight',
            name='complete',
            field=models.BooleanField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='orderflight',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
