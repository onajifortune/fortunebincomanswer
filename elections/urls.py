from django.urls import path

from . import views

urlpatterns = [
    path('', views.list_polling_units, name='polling_units'),
    path('polling_units/<int:uniqueid>', views.retrieve_polling_unit, name='polling_unit'),
    path('local_govt', views.local_government, name='local_govt'),
    path('add_results', views.result_for_new_polling_unit, name='add_results'),
    ]
