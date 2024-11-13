from django.urls import path
from application.views import (
    index, success_action, faill_action, assign, do_assign, reset_today, sent_to_channel
)
app_name = 'application'

urlpatterns = [
    path('', index, name='index'),
    path('success/', success_action, name='success_action'),
    path('faill/', faill_action, name='faill_action'),
    path('assign/', assign, name='assign'),
    path('do_assign/', do_assign, name='do_assign'),
    path('reset_today/', reset_today, name='reset_today'),
    path('reset_today/', reset_today, name='reset_today'),
    path('sent_to_channel/', sent_to_channel, name='sent_to_channel'),
]
