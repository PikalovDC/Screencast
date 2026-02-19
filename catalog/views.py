from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
from catalog.models import Product, Category
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, View


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class HomeListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'page_obj'
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        all_products = Product.objects.all()
        context['total_products'] = all_products.count()
        context['categories_count'] = all_products.values('category').distinct().count()
        return context


class ContactsView(View):
    def get(self, request):
        return render(request, 'catalog/contacts.html')

    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        return HttpResponse(f"Спасибо, {name}, Ваше обращение получено.")
