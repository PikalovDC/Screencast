from django.urls import path, include
from catalog.apps import CatalogConfig
from . import views
from .views import ProductDetailView, HomeListView, ContactsView

app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('product_detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail')
]
