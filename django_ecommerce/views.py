from django.shortcuts import render

from store.models import Product


def home(request):
    #Desplegar los productos en el Home, pero que sean solo los productos activos
    products = Product.objects.all().filter(is_available =True)

    context = {
        'products': products,
    }

    return render(request, 'home.html', context)