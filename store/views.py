from django.shortcuts import render, get_object_or_404

from store.models import Product
from category.models import Category

# Create your views here.
def store(request, category_slug=None):
    #filtrar la consulta de productos por el tipo de categoria
    categories = None
    products = None

    # si no es nulo significa que si tiene un slug para filtrar
    if category_slug != None:
        #esta es una funcionde ython la cual me busca el slug si existe filtar todo
        #lo relacionado con ese prodcuto sino da error 404
        categories = get_object_or_404(Category, slug=category_slug)

        # que category sea igual al que me estam pidiendo category_slug, tambien otra condicion
        # es que el producto este habilitado
        products = Product.objects.filter(category=categories, is_available=True)
        #Tambien queiro saber la cantidadd de prodcutos con ese slug
        product_count = products.count()
    else:
        # Mostrando todos los productos en la store
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()

    context = {
        'products' : products,
        'product_count': product_count
    }
    return render(request,'store/store.html',context)


def product_detail(request, category_slug, product_slug):
    #DEBO HACER UNA VALIDACION EN CASO DE QUE EL PRODUCTO QUE SE ESTE CONSULTANDO YA NO EXISTA
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e
    context = {
        'single_product': single_product,
    }
    return render(request, 'store/product_detail.html',context)