from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('detail/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail')
]
