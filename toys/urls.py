from django.urls import path
from . import views

urlpatterns = [
    path('', views.toy_list, name="toy_list"),
    path('<int:id>', views.toy_detail, name='toy_detail'),
]