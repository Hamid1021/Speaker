# Generated by Django 5.1.3 on 2024-11-12 19:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0009_alter_speaker_education_attendees_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(blank=True, null=True, verbose_name='تاریخ'),
        ),
        migrations.AlterField(
            model_name='order',
            name='time',
            field=models.TimeField(blank=True, null=True, verbose_name='زمان'),
        ),
        migrations.CreateModel(
            name='OrderSpeaker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='زمان ثبت')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='application.order', verbose_name='سفارش')),
                ('speaker', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='application.speaker', verbose_name='سخنران')),
            ],
            options={
                'verbose_name': 'سخنران_سفارش',
                'verbose_name_plural': 'اختصاص سفارش به سخنران',
            },
        ),
    ]
