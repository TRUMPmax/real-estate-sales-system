from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('create/', views.property_create, name='property_create'),
    path('<int:pk>/', views.property_detail, name='property_detail'),
    path('<int:pk>/update/', views.property_update, name='property_update'),
    path('<int:pk>/delete/', views.property_delete, name='property_delete'),
    path('<int:pk>/price/', views.price_update, name='price_update'),
    path('<int:pk>/image/upload/', views.property_image_upload, name='image_upload'),
    path('<int:pk>/image/<int:image_id>/delete/', views.property_image_delete, name='image_delete'),
]

