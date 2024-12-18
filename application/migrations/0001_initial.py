# Generated by Django 5.1.3 on 2024-12-14 00:59

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_id', models.IntegerField(blank=True, default=0, null=True, unique=True, verbose_name='id')),
                ('username', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='username')),
                ('m_type', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='type')),
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
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, default='', max_length=15, null=True, verbose_name='شماره همراه')),
                ('date', models.DateField(blank=True, null=True, verbose_name='تاریخ')),
                ('time', models.TimeField(blank=True, null=True, verbose_name='زمان')),
                ('num_attendees', models.IntegerField(blank=True, default=0, null=True, verbose_name='تعداد اعضای جلسه')),
                ('gender_attendees', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='جنسیت حضار')),
                ('education_min_attendees', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='حداقل سواد حاضران')),
                ('education_max_attendees', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='حداکثر سواد حاضران')),
                ('city', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='شهر')),
                ('topic', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='موضوع روضه')),
                ('status', models.CharField(choices=[('uc', 'انجام نشده'), ('c', 'انجام شده')], default='uc', max_length=2, verbose_name='وضعیت انجام')),
                ('is_assign', models.BooleanField(default=False, verbose_name='مرتبط شده؟')),
                ('is_message_send', models.BooleanField(default=False, verbose_name='پیام ارسال شده؟')),
                ('related_message', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='application.channelmessage', verbose_name='پیام مرتبط')),
            ],
            options={
                'verbose_name': 'سفارش',
                'verbose_name_plural': 'سفارشات ثبت شده',
                'ordering': ['-pk', 'date', 'time'],
            },
        ),
        migrations.CreateModel(
            name='Speaker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='نام')),
                ('family', models.CharField(blank=True, max_length=255, null=True, verbose_name='نام خانوادگی')),
                ('age', models.IntegerField(blank=True, default=0, null=True, verbose_name='سن')),
                ('phone', models.CharField(blank=True, default='+98912345689', max_length=12, null=True, verbose_name='شماره همراه')),
                ('address', models.CharField(blank=True, default='ثبت نشده', max_length=500, null=True, verbose_name='آدرس')),
                ('education_attendees', models.CharField(blank=True, default='نا مشخص', max_length=255, null=True, verbose_name='تحصیلات سخنران')),
                ('register_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='زمان ثبت نام')),
                ('total_number_of_lectures', models.IntegerField(blank=True, default=0, null=True, verbose_name='تعداد کل روضه های انجام شده')),
                ('status', models.BooleanField(default=True, verbose_name='وضعیت فعالیت')),
                ('is_deleted', models.BooleanField(default=False, editable=False, verbose_name='حذف شده؟')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'سخنران',
                'verbose_name_plural': 'سخنران ها',
                'ordering': ['name', 'family', 'age', 'total_number_of_lectures'],
            },
        ),
        migrations.CreateModel(
            name='SelectOrderSpeaker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.ManyToManyField(blank=True, related_name='order_set', to='application.order', verbose_name='سفارش')),
                ('speaker', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.DO_NOTHING, to='application.speaker', verbose_name='سخنران')),
            ],
            options={
                'verbose_name': 'انتخاب سفارش',
                'verbose_name_plural': 'سفارشات انتخاب شده',
            },
        ),
        migrations.CreateModel(
            name='AssignOrderSpeaker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='زمان ثبت')),
                ('is_message_send', models.BooleanField(default=False, verbose_name='پیام ارسال شده؟')),
                ('related_message', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='application.channelmessage', verbose_name='پیام مرتبط')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='application.order', verbose_name='سفارش')),
                ('speaker', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='application.speaker', verbose_name='سخنران')),
            ],
            options={
                'verbose_name': 'سخنران_سفارش',
                'verbose_name_plural': 'اختصاص سفارش به سخنران',
            },
        ),
    ]
