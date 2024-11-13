# Generated by Django 5.1.3 on 2024-11-11 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_order_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['status', '-date', '-time'], 'verbose_name': 'سفارش', 'verbose_name_plural': 'سفارشات ثبت شده'},
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('uc', 'انجام نشده'), ('c', 'انجام شده')], default='', max_length=2, null=True, verbose_name='وضعیت'),
        ),
    ]