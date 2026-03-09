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
        return Product.objects.filter(is_published=True)

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
