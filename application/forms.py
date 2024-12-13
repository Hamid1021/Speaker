from django import forms
from application.Entities.order_model import OrderSpeaker

class OrderSpeakerForm(forms.ModelForm):
    class Meta:
        model = OrderSpeaker
        fields = ["speaker",]
