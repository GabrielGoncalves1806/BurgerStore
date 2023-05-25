from django.urls import path

from . import views
urlpatterns = [
    path('', views.DeliveryList.as_view(), name='delivery-list'),
    path('test/', views.test, name='test'),
]