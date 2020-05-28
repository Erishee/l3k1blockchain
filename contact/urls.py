from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('api_instruction',views.api_instruction,name='api_instruction')
]