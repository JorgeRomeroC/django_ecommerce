from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    # para poder filtrar por categoria, necesito pasar el slug por la url
    path('<slug:category_slug>/',views.store, name='products_by_category'),
    # PARA VER EL DETALLE DEL PRODCUTOS
    path('<slug:category_slug>/<slug:product_slug>/',views.product_detail, name='product_detail'),
]