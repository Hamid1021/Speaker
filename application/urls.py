from django.urls import path
from application.views import index
app_name = 'application'

urlpatterns = [
    path('', index, name='index'),
]
