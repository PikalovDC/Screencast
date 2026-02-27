from django.urls import path, include
from catalog.apps import CatalogConfig
from . import views
from .views import ProductDetailView, HomeListView, ContactsView, ProductUpdateView, ProductCreateView, ProductDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('', HomeListView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('product_detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail')
]
