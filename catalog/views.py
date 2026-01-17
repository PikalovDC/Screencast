from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'catalog/home.html')

def contacts(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')

        return HttpResponse(f"Спасибо, {name}, Ваше обращение получено.")
    return render(request, 'catalog/contacts.html')