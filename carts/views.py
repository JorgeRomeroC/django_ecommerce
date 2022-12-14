from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404

from carts.models import Cart, CartItem
from store.models import Product

#================================================
# CREAMOS LA SESSION
#================================================
def _cart_id(request):
    #guardamos la session en cart
    cart = request.session.session_key
    # si NO existe la session entonces creala
    if not cart:
        cart = request.session.create()
    return cart

#================================================
#ESTA FUNCION (add_cart) SE EJECUTARA AL MOMENTO DE EL CLIENYE DE CLICK
# EN EL BOTON AGRFEGAR AL CARRITO, ESTO GRABARA EN LA BASE DE DATODS3
# LA CREACION DE ESE CARRITO
#================================================


# EL CARRITO SE CREARA EN BASE AÑ product_id
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    # validamos si el carrito existe, sino hay que crearlo
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        #indicamos la cantidad de prodcutos que elejimos
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity= 1,
            cart = cart
        )
        cart_item.save()
    return redirect('cart')

#================================================
# FUNCION PARA REMOVER EL PRODCUTO DEL CARRITO
# O DISMINUIR CON EL BOTON - (MENOS
#================================================

def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id((request)))
    product = get_object_or_404(Product, id=product_id)
    #buscar el carrito de compras por el prodcuto y en funcion del carrito
    cart_item = CartItem.objects.get(product=product, cart=cart)

    #Sera utilizada en el boton de restar cantidad de prodcutos de un elemento
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        # si es menor a 1 es 0, por lo tanto que se elimine
        cart_item.delete()
    return redirect('cart', )

#================================================
# FUNCION PARA DAR ACCION AL BOTON ELIMINAR DEL CARRITO
#================================================
def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')

#================================================
# FUNCION PARA CALCULAR EL PRECIO TOTAL, FINAL Y EL IVA POR PRODCUTO
#================================================
def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        # queremos dsaber el precio total de mis productos y cantidad total qeu tiene el carrito y su IVA
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        iva = (2*total)/19
        grand_total = total + iva
    except ObjectDoesNotExist:
        pass #solo ignora la eception

    context = {
        'total': total,
        'quantity':quantity,
        'cart_items': cart_items,
        'iva' : iva,
        'grand_total': grand_total

    }

    return render(request, 'store/cart.html',context)