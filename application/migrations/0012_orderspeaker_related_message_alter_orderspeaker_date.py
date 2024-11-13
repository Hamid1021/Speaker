# Generated by Django 5.1.3 on 2024-11-12 21:52

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0011_order_is_assign'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderspeaker',
            name='related_message',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='application.channelmessage', verbose_name='پیام مرتبط'),
        ),
        migrations.AlterField(
            model_name='orderspeaker',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 11, 12, 21, 52, 39, 999648, tzinfo=datetime.timezone.utc), null=True, verbose_name='زمان ثبت'),
        ),
    ]
