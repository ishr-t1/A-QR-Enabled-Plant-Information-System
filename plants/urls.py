from django.urls import path
from . import views

app_name = 'plants'
urlpatterns = [
    path('', views.home, name='home'),
    path('plant/<int:plant_id>/',views.plant_detail, name='plant_detail'),

]