from django.contrib import admin
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from application.Entities.order_model import Order

# "order","speaker","date","is_message_send"
class OrderSpeakerAdmin(admin.ModelAdmin):
    list_display = ["speaker","date","jdate","is_message_send"]
    readonly_fields = ["date", "is_message_send"]
    filter_horizontal = ['order',]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        self.update_orders(form.instance)

    def update_orders(self, obj):
        for order in obj.order.all():
            order.is_selected = True
            order.save()

    # اتصال سیگنال‌ها به مدل OrderSpeaker
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        m2m_changed.connect(self.orders_changed, sender=obj.order.through)
    
    def orders_changed(self, sender, instance, action, **kwargs):
        if action == 'post_remove':
            for order_id in kwargs['pk_set']:
                Order.objects.make_as_not_selected(order_id)
