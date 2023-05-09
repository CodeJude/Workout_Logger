from django.urls import path
from . import views

urlpatterns = [
    path('', views.log_workout, name='log_workout'),
    path('fetch/', views.fetch_api_data, name='fetch'),
]
