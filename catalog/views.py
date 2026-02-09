from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
from catalog.models import Product, Category

def home(request):
    all_products  = Product.objects.all()
    paginator = Paginator(all_products , 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories_count = all_products.values('category').distinct().count()
    context = {
        'page_obj': page_obj,
        'total_products': all_products.count(),
        'categories_count': categories_count,
    }
    return render(request, 'catalog/home.html', context=context)

def contacts(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')

        return HttpResponse(f"Спасибо, {name}, Ваше обращение получено.")
    return render(request, 'catalog/contacts.html')

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {
        'product': product
    }
    return render(request, 'catalog/product_detail.html', context=context)
