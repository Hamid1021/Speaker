# Generated by Django 5.1.3 on 2024-12-08 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0017_alter_order_options_alter_orderspeaker_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_selected',
            field=models.BooleanField(default=False, verbose_name='پیام ارسال شده؟'),
        ),
        migrations.RemoveField(
            model_name='orderspeaker',
            name='order',
        ),
        migrations.AddField(
            model_name='orderspeaker',
            name='order',
            field=models.ManyToManyField(to='application.order', verbose_name='سفارش'),
        ),
    ]
