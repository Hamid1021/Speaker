# Generated by Django 5.1.3 on 2024-12-09 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0018_order_is_selected_remove_orderspeaker_order_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='is_selected',
            field=models.BooleanField(default=False, verbose_name='انتخاب شده'),
        ),
        migrations.AlterField(
            model_name='orderspeaker',
            name='order',
            field=models.ManyToManyField(blank=True, null=True, related_name='order_set', to='application.order', verbose_name='سفارش'),
        ),
    ]