from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect
from catalog.models import Product, Category
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, View
from .forms import ProductForm
from django.contrib import messages
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .services import ProductService
from django.core.cache import cache


class CategoryProductsView(ListView):
    model = Product
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        cache_key = f'category_products_{category_id}'

        products = cache.get(cache_key)
        if not products:
            products = Product.objects.filter(category_id=category_id, is_published=True)
            cache.set(cache_key, products, 300)

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')

        # Кешируем категорию
        cache_key = f'category_{category_id}'
        category = cache.get(cache_key)
        if not category:
            category = get_object_or_404(Category, id=category_id)
            cache.set(cache_key, category, 600)

        context['category'] = category

        # Кешируем список категорий для бокового меню
        categories = cache.get('all_categories')
        if not categories:
            categories = Category.objects.all()
            cache.set('all_categories', categories, 600)

        context['categories'] = categories

        return context

class ProductUnpublishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'catalog.can_unpublish_product'

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_published = False
        product.save()
        messages.success(request, f'Публикация товара "{product.title}" отменена')
        return redirect('catalog:product_detail', pk=pk)

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    login_url = 'users:login'
    redirect_field_name = 'next'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.is_published = False
        messages.success(self.request, 'Товар успешно создан')
        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def dispatch(self, request, *args, **kwargs):
        """Проверка прав доступа"""
        product = self.get_object()
        # Проверяем, является ли пользователь владельцем
        if product.owner != request.user:
            messages.error(request, 'Вы не можете редактировать этот товар, так как не являетесь его владельцем')
            return redirect('catalog:product_detail', pk=product.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Товар успешно обновлен!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})

class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')
    context_object_name = 'product'
    permission_required = 'catalog.delete_product'

    def dispatch(self, request, *args, **kwargs):
        """Проверка прав доступа"""
        product = self.get_object()
        # Проверяем: владелец ИЛИ модератор (с правом delete_product)
        if product.owner != request.user and not request.user.has_perm('catalog.delete_product'):
            messages.error(request, 'У вас нет прав для удаления этого товара')
            return redirect('catalog:product_detail', pk=product.pk)
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Товар успешно удален!')
        return super().delete(request, *args, **kwargs)


@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class HomeListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'page_obj'
    paginate_by = 6

    def get_queryset(self):

        products = cache.get('home_products')
        if not products:
            products = Product.objects.filter(is_published=True)
            cache.set('home_products', products, 300)

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Кешируем статистику
        stats = cache.get('home_stats')
        if not stats:
            all_products = Product.objects.all()
            total_products = all_products.count()
            categories_count = all_products.values('category').distinct().count()
            stats = {
                'total_products': total_products,
                'categories_count': categories_count,
            }
            cache.set('home_stats', stats, 300)

        context['total_products'] = stats['total_products']
        context['categories_count'] = stats['categories_count']

        # Кешируем список категорий
        categories = cache.get('all_categories')
        if not categories:
            categories = Category.objects.all()
            cache.set('all_categories', categories, 600)  # 10 минут

        context['categories'] = categories

        return context

class ContactsView(View):
    def get(self, request):
        return render(request, 'catalog/contacts.html')

    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        return HttpResponse(f"Спасибо, {name}, Ваше обращение получено.")
