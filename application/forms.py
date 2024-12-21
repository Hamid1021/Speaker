from django import forms
from application.Entities.order_model import SelectOrderSpeaker, Order
from application.Entities.Speaker_model import Speaker
from application.Entities.order_model import AssignOrderSpeaker
from account.models import USER

class SelectOrderSpeakerForm(forms.ModelForm):
    class Meta:
        model = SelectOrderSpeaker
        fields = ['order']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SelectOrderSpeakerForm, self).__init__(*args, **kwargs)
        # فیلتر سفارشات اختصاص داده نشده
        self.fields['order'].queryset = Order.objects.get_all_not_assign()
        if user:
            get_speaker = Speaker.objects.filter(user=user).first()
            if get_speaker:
                self.instance.speaker = get_speaker


class OrderSpeakerForm(forms.ModelForm):
    class Meta:
        model = AssignOrderSpeaker
        fields = ['speaker']

