from django.urls import path
from application.views import (
    index, success_action, faill_action, assign, edit_assign, do_assign, sent_to_channel, list_assign,
    select_order_by_speaker, success_select_order, speaker_assigned_orders, change_status
)
app_name = 'application'

urlpatterns = [
    path('', index, name='index'),
    path('success/', success_action, name='success_action'),
    path('faill/', faill_action, name='faill_action'),
    path('assign/', assign, name='assign'),
    path('assign/<int:pk>/', edit_assign, name='edit_assign'),
    path('list_assign/', list_assign, name='list_assign'),
    path('do_assign/', do_assign, name='do_assign'),
    path('sent_to_channel/', sent_to_channel, name='sent_to_channel'),
    path('select/', select_order_by_speaker, name='select_order_by_speaker'),
    path('success_select_order/', success_select_order, name='success_select_order'),
    path('assigned_orders/<int:speaker_id>/', speaker_assigned_orders, name='speaker_assigned_orders'),
    path('change_status/<int:speaker_id>/<int:order_id>/', change_status, name='change_status'),
]
