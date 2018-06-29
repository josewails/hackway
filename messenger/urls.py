from django.urls import path

from .views import (
    webhook,
    send_coding_results
)

urlpatterns = [
    path('webhook', webhook, name='webhook'),
    path('send_coding_results', send_coding_results, name='send_coding_results')
]