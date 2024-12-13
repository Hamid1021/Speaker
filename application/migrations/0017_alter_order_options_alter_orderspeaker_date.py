# Generated by Django 5.1.3 on 2024-12-08 12:37

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0016_remove_speaker_today_number_of_lectures_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-pk', 'date', 'time'], 'verbose_name': 'سفارش', 'verbose_name_plural': 'سفارشات ثبت شده'},
        ),
        migrations.AlterField(
            model_name='orderspeaker',
            name='date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='زمان ثبت'),
        ),
    ]