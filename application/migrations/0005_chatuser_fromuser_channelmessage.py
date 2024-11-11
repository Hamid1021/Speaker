# Generated by Django 5.1.3 on 2024-11-11 16:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0004_alter_order_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_id', models.IntegerField(blank=True, default=0, null=True, unique=True, verbose_name='id')),
                ('username', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='username')),
                ('type', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='type')),
            ],
            options={
                'verbose_name': 'چت',
                'verbose_name_plural': 'چت مخاطبین',
            },
        ),
        migrations.CreateModel(
            name='FromUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_id', models.IntegerField(blank=True, default=0, null=True, unique=True, verbose_name='id')),
                ('is_bot', models.BooleanField(blank=True, default=False, null=True, verbose_name='is_bot')),
                ('first_name', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='first_name')),
                ('last_name', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='last_name')),
                ('username', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='username')),
                ('can_join_groups', models.BooleanField(blank=True, null=True, verbose_name='can_join_groups')),
                ('can_read_all_group_messages', models.BooleanField(blank=True, null=True, verbose_name='can_read_all_group_messages')),
                ('supports_inline_queries', models.BooleanField(blank=True, null=True, verbose_name='supports_inline_queries')),
            ],
            options={
                'verbose_name': 'مخاطب',
                'verbose_name_plural': 'مخاطبین',
            },
        ),
        migrations.CreateModel(
            name='ChannelMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_id', models.IntegerField(blank=True, default=0, null=True, verbose_name='message_id')),
                ('date', models.CharField(blank=True, max_length=12, null=True, verbose_name='date')),
                ('text', models.TextField(blank=True, default='', null=True, verbose_name='text')),
                ('status', models.CharField(blank=True, choices=[('s', 'ارسال شد'), ('us', 'ارسال نشد')], default='us', max_length=2, null=True, verbose_name='ok')),
                ('chat_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='application.chatuser')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='application.fromuser')),
            ],
            options={
                'verbose_name': 'پیام',
                'verbose_name_plural': 'پیام های ارسال شده',
            },
        ),
    ]
